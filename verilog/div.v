module div #(parameter DATA_WIDTH=1, parameter BIN_POS=1) (input wire clk, input wire rst, output reg ready = 1, output reg complete = 0, input wire [DATA_WIDTH-1:0] a, input wire [DATA_WIDTH-1:0] b, output reg [DATA_WIDTH-1:0] out = 0, output wire div_zero);

    reg [DATA_WIDTH-1:0] count = 0;
    reg [DATA_WIDTH-1:0] i = 0;

    reg [DATA_WIDTH*2-1:0] zero = 0;

    reg [DATA_WIDTH*2-1:0] num;
    reg [DATA_WIDTH*2-1:0] denom;

    reg [DATA_WIDTH*2-1:0] remainder = 0;
    reg [DATA_WIDTH*2-1:0] quot = 0;
    wire sign_neg;

    wire sign_a_neg;
    wire sign_b_neg;
    wire [DATA_WIDTH-1:0] a_neg;
    wire [DATA_WIDTH-1:0] b_neg;

    assign a_neg = ~a+1;
    assign b_neg = ~b+1;

    assign sign_a_neg = a >> (DATA_WIDTH-1);
    assign sign_b_neg = b >> (DATA_WIDTH-1);
    assign sign_neg = sign_a_neg ^ sign_b_neg;

    assign div_zero = b == 0;

    always @(posedge clk)
    begin
        if (rst || b == 0)
        begin
            ready = 1;
            count = 0;
            i = 0;
            complete = 0;
            quot = 0;
            out = 0;
            remainder = 0;

        end
        else if (!complete)
        begin
            ready = 0;

            if (count == 0)
            begin
                num = {sign_a_neg ? a_neg : a, {DATA_WIDTH{1'b0}}};
                denom = {{DATA_WIDTH{1'b0}}, sign_b_neg ? b_neg : b};
            end
            i = DATA_WIDTH * 2 - count - 1;
            remainder = remainder << 1;
            remainder[0] = num[i];
            if (remainder >= denom)
            begin
                remainder = remainder - denom;
                quot[i] = 1;
            end

            count += 1;

            if (count == DATA_WIDTH * 2)
            begin
                //Take the centre of the enlarged range
                out = quot[DATA_WIDTH*2-1-DATA_WIDTH/2:DATA_WIDTH/2];
                if (sign_neg)
                begin
                    out = ~out + 1;
                end
                complete = 1;
            end
        end
    end
endmodule
