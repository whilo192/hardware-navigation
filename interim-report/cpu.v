module cpu(input wire clk, output reg [7:0] data_out, output reg data_out_new);
    reg [11:0] pc;
    
    reg [4095:0] mem;
    
    reg [11:0] indirect_address;
    reg [11:0] indirect_address_lhs;
    reg [11:0] indirect_address_rhs;
    
    //In real life we'd have a memory module or something - but for now we'll just program the memory here
    initial begin
        pc = 0;
        indirect_address = 0;
        
        mem = 4096'h0;
        
        mem[0*8+:8] = 8'h6; //Set position f0 to 16
        mem[1*8+:8] = 8'hf0;
        mem[2*8+:8] = 8'h10;
        
        mem[3*8+:8] = 8'h5; //Print the number at f0
        mem[4*8+:8] = 8'hf0;
        
        mem[5*8+:8] = 8'h4; //If f0 is 0, jump to e0
        mem[6*8+:8] = 8'hf0;
        mem[7*8+:8] = 8'he0;
        
        mem[8*8+:8] = 8'h1; //Else subtract 1 (in f1) from f0, store in f0
        mem[9*8+:8] = 8'hf0;
        mem[10*8+:8] = 8'hf0;
        mem[11*8+:8] = 8'hf1;
        
        mem[12*8+:8] = 8'h3; //Jump back to index 3
        mem[13*8+:8] = 8'h3;
        
        mem[224*8+:8] = 8'h3; //e0 is jump to e0 (a spinlock)
        mem[225*8+:8] = 8'he0;
        
        mem[241*8+:8] = 8'h1; //f1 is 1 (to subtract 1)
    end
    
    always @(posedge clk)
    begin
        data_out_new = 0;
        
        if (mem[pc+:8] == 8'h0) //Add dst a b
        begin
            indirect_address = mem[pc+8+:8] * 8;
            indirect_address_lhs = mem[pc+16+:8] * 8;
            indirect_address_rhs = mem[pc+24+:8] * 8;
            
            mem[indirect_address+:8] = mem[indirect_address_lhs+:8] + mem[indirect_address_rhs+:8];
            pc += 8'h20;
        end
        else if (mem[pc+:8] == 8'h1) //Sub dst a b
        begin
            indirect_address = mem[pc+8+:8] * 8;
            indirect_address_lhs = mem[pc+16+:8] * 8;
            indirect_address_rhs = mem[pc+24+:8] * 8;
            
            mem[indirect_address+:8] = mem[indirect_address_lhs+:8] - mem[indirect_address_rhs+:8];
            
            pc += 8'h20;
        end
        else if (mem[pc+:8] == 8'h3) //Jump addr
        begin
            pc = mem[pc+8+:8] * 8;
        end
        else if (mem[pc+:8] == 8'h4) //Jump addr if a is 0
        begin
            indirect_address = mem[pc+8+:8] * 8;
            
            if (mem[indirect_address+:8] == 0)
            begin
                pc = mem[pc+16+:8] * 8;
            end
            else
            begin
                pc += 8'h18;
            end
        end
        else if (mem[pc+:8] == 8'h5) //Output data
        begin
            indirect_address = mem[pc+8+:8] * 8;
            data_out = mem[indirect_address+:8];
            data_out_new = 1;
            pc += 8'h10;
        end
        else if (mem[pc+:8] == 8'h6) //Set mem location x to value
        begin
            indirect_address = mem[pc+8+:8] * 8;
            mem[indirect_address+:8] = mem[pc+16+:8];
            pc += 8'h18;
        end
        else
        begin //if no opcodes match then do nothing
            pc += 8'h8;
        end
    end
endmodule
