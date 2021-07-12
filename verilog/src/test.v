module test;
    reg [127:0] matrix;

    wire [7:0] det;

    matdet4 m1(matrix, det);

    initial begin;
        matrix = {8'd1, 8'd2, 8'd3, 8'd5, 8'd1, 8'd5, 8'd7, 8'd4, 8'd1, 8'd1, 8'd2, 8'd3, 8'd4, 8'd5, 8'd6, 8'd7};

        #1

        $display(det);
        $finish;
    end
endmodule
