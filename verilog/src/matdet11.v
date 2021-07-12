module matdet11 #(parameter DATA_WIDTH=8, parameter MATRIX_SIZE=121) (input wire [(MATRIX_SIZE * DATA_WIDTH) - 1:0] a, output wire [DATA_WIDTH-1:0] det);
wire [DATA_WIDTH-1:0] w0, w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14, w15, w16, w17, w18, w19, w20, w21, w22, w23, w24, w25, w26, w27, w28, w29, w30, w31;
matdet10 md0({a[103:96], a[111:104], a[119:112], a[127:120], a[135:128], a[143:136], a[151:144], a[159:152], a[167:160], a[175:168], a[191:184], a[199:192], a[207:200], a[215:208], a[223:216], a[231:224], a[239:232], a[247:240], a[255:248], a[263:256], a[279:272], a[287:280], a[295:288], a[303:296], a[311:304], a[319:312], a[327:320], a[335:328], a[343:336], a[351:344], a[367:360], a[375:368], a[383:376], a[391:384], a[399:392], a[407:400], a[415:408], a[423:416], a[431:424], a[439:432], a[455:448], a[463:456], a[471:464], a[479:472], a[487:480], a[495:488], a[503:496], a[511:504], a[519:512], a[527:520], a[543:536], a[551:544], a[559:552], a[567:560], a[575:568], a[583:576], a[591:584], a[599:592], a[607:600], a[615:608], a[631:624], a[639:632], a[647:640], a[655:648], a[663:656], a[671:664], a[679:672], a[687:680], a[695:688], a[703:696], a[719:712], a[727:720], a[735:728], a[743:736], a[751:744], a[759:752], a[767:760], a[775:768], a[783:776], a[791:784], a[807:800], a[815:808], a[823:816], a[831:824], a[839:832], a[847:840], a[855:848], a[863:856], a[871:864], a[879:872], a[895:888], a[903:896], a[911:904], a[919:912], a[927:920], a[935:928], a[943:936], a[951:944], a[959:952], a[967:960]}, w0);
matdet10 md1({a[95:88], a[111:104], a[119:112], a[127:120], a[135:128], a[143:136], a[151:144], a[159:152], a[167:160], a[175:168], a[183:176], a[199:192], a[207:200], a[215:208], a[223:216], a[231:224], a[239:232], a[247:240], a[255:248], a[263:256], a[271:264], a[287:280], a[295:288], a[303:296], a[311:304], a[319:312], a[327:320], a[335:328], a[343:336], a[351:344], a[359:352], a[375:368], a[383:376], a[391:384], a[399:392], a[407:400], a[415:408], a[423:416], a[431:424], a[439:432], a[447:440], a[463:456], a[471:464], a[479:472], a[487:480], a[495:488], a[503:496], a[511:504], a[519:512], a[527:520], a[535:528], a[551:544], a[559:552], a[567:560], a[575:568], a[583:576], a[591:584], a[599:592], a[607:600], a[615:608], a[623:616], a[639:632], a[647:640], a[655:648], a[663:656], a[671:664], a[679:672], a[687:680], a[695:688], a[703:696], a[711:704], a[727:720], a[735:728], a[743:736], a[751:744], a[759:752], a[767:760], a[775:768], a[783:776], a[791:784], a[799:792], a[815:808], a[823:816], a[831:824], a[839:832], a[847:840], a[855:848], a[863:856], a[871:864], a[879:872], a[887:880], a[903:896], a[911:904], a[919:912], a[927:920], a[935:928], a[943:936], a[951:944], a[959:952], a[967:960]}, w1);
matdet10 md2({a[95:88], a[103:96], a[119:112], a[127:120], a[135:128], a[143:136], a[151:144], a[159:152], a[167:160], a[175:168], a[183:176], a[191:184], a[207:200], a[215:208], a[223:216], a[231:224], a[239:232], a[247:240], a[255:248], a[263:256], a[271:264], a[279:272], a[295:288], a[303:296], a[311:304], a[319:312], a[327:320], a[335:328], a[343:336], a[351:344], a[359:352], a[367:360], a[383:376], a[391:384], a[399:392], a[407:400], a[415:408], a[423:416], a[431:424], a[439:432], a[447:440], a[455:448], a[471:464], a[479:472], a[487:480], a[495:488], a[503:496], a[511:504], a[519:512], a[527:520], a[535:528], a[543:536], a[559:552], a[567:560], a[575:568], a[583:576], a[591:584], a[599:592], a[607:600], a[615:608], a[623:616], a[631:624], a[647:640], a[655:648], a[663:656], a[671:664], a[679:672], a[687:680], a[695:688], a[703:696], a[711:704], a[719:712], a[735:728], a[743:736], a[751:744], a[759:752], a[767:760], a[775:768], a[783:776], a[791:784], a[799:792], a[807:800], a[823:816], a[831:824], a[839:832], a[847:840], a[855:848], a[863:856], a[871:864], a[879:872], a[887:880], a[895:888], a[911:904], a[919:912], a[927:920], a[935:928], a[943:936], a[951:944], a[959:952], a[967:960]}, w2);
matdet10 md3({a[95:88], a[103:96], a[111:104], a[127:120], a[135:128], a[143:136], a[151:144], a[159:152], a[167:160], a[175:168], a[183:176], a[191:184], a[199:192], a[215:208], a[223:216], a[231:224], a[239:232], a[247:240], a[255:248], a[263:256], a[271:264], a[279:272], a[287:280], a[303:296], a[311:304], a[319:312], a[327:320], a[335:328], a[343:336], a[351:344], a[359:352], a[367:360], a[375:368], a[391:384], a[399:392], a[407:400], a[415:408], a[423:416], a[431:424], a[439:432], a[447:440], a[455:448], a[463:456], a[479:472], a[487:480], a[495:488], a[503:496], a[511:504], a[519:512], a[527:520], a[535:528], a[543:536], a[551:544], a[567:560], a[575:568], a[583:576], a[591:584], a[599:592], a[607:600], a[615:608], a[623:616], a[631:624], a[639:632], a[655:648], a[663:656], a[671:664], a[679:672], a[687:680], a[695:688], a[703:696], a[711:704], a[719:712], a[727:720], a[743:736], a[751:744], a[759:752], a[767:760], a[775:768], a[783:776], a[791:784], a[799:792], a[807:800], a[815:808], a[831:824], a[839:832], a[847:840], a[855:848], a[863:856], a[871:864], a[879:872], a[887:880], a[895:888], a[903:896], a[919:912], a[927:920], a[935:928], a[943:936], a[951:944], a[959:952], a[967:960]}, w3);
matdet10 md4({a[95:88], a[103:96], a[111:104], a[119:112], a[135:128], a[143:136], a[151:144], a[159:152], a[167:160], a[175:168], a[183:176], a[191:184], a[199:192], a[207:200], a[223:216], a[231:224], a[239:232], a[247:240], a[255:248], a[263:256], a[271:264], a[279:272], a[287:280], a[295:288], a[311:304], a[319:312], a[327:320], a[335:328], a[343:336], a[351:344], a[359:352], a[367:360], a[375:368], a[383:376], a[399:392], a[407:400], a[415:408], a[423:416], a[431:424], a[439:432], a[447:440], a[455:448], a[463:456], a[471:464], a[487:480], a[495:488], a[503:496], a[511:504], a[519:512], a[527:520], a[535:528], a[543:536], a[551:544], a[559:552], a[575:568], a[583:576], a[591:584], a[599:592], a[607:600], a[615:608], a[623:616], a[631:624], a[639:632], a[647:640], a[663:656], a[671:664], a[679:672], a[687:680], a[695:688], a[703:696], a[711:704], a[719:712], a[727:720], a[735:728], a[751:744], a[759:752], a[767:760], a[775:768], a[783:776], a[791:784], a[799:792], a[807:800], a[815:808], a[823:816], a[839:832], a[847:840], a[855:848], a[863:856], a[871:864], a[879:872], a[887:880], a[895:888], a[903:896], a[911:904], a[927:920], a[935:928], a[943:936], a[951:944], a[959:952], a[967:960]}, w4);
matdet10 md5({a[95:88], a[103:96], a[111:104], a[119:112], a[127:120], a[143:136], a[151:144], a[159:152], a[167:160], a[175:168], a[183:176], a[191:184], a[199:192], a[207:200], a[215:208], a[231:224], a[239:232], a[247:240], a[255:248], a[263:256], a[271:264], a[279:272], a[287:280], a[295:288], a[303:296], a[319:312], a[327:320], a[335:328], a[343:336], a[351:344], a[359:352], a[367:360], a[375:368], a[383:376], a[391:384], a[407:400], a[415:408], a[423:416], a[431:424], a[439:432], a[447:440], a[455:448], a[463:456], a[471:464], a[479:472], a[495:488], a[503:496], a[511:504], a[519:512], a[527:520], a[535:528], a[543:536], a[551:544], a[559:552], a[567:560], a[583:576], a[591:584], a[599:592], a[607:600], a[615:608], a[623:616], a[631:624], a[639:632], a[647:640], a[655:648], a[671:664], a[679:672], a[687:680], a[695:688], a[703:696], a[711:704], a[719:712], a[727:720], a[735:728], a[743:736], a[759:752], a[767:760], a[775:768], a[783:776], a[791:784], a[799:792], a[807:800], a[815:808], a[823:816], a[831:824], a[847:840], a[855:848], a[863:856], a[871:864], a[879:872], a[887:880], a[895:888], a[903:896], a[911:904], a[919:912], a[935:928], a[943:936], a[951:944], a[959:952], a[967:960]}, w5);
matdet10 md6({a[95:88], a[103:96], a[111:104], a[119:112], a[127:120], a[135:128], a[151:144], a[159:152], a[167:160], a[175:168], a[183:176], a[191:184], a[199:192], a[207:200], a[215:208], a[223:216], a[239:232], a[247:240], a[255:248], a[263:256], a[271:264], a[279:272], a[287:280], a[295:288], a[303:296], a[311:304], a[327:320], a[335:328], a[343:336], a[351:344], a[359:352], a[367:360], a[375:368], a[383:376], a[391:384], a[399:392], a[415:408], a[423:416], a[431:424], a[439:432], a[447:440], a[455:448], a[463:456], a[471:464], a[479:472], a[487:480], a[503:496], a[511:504], a[519:512], a[527:520], a[535:528], a[543:536], a[551:544], a[559:552], a[567:560], a[575:568], a[591:584], a[599:592], a[607:600], a[615:608], a[623:616], a[631:624], a[639:632], a[647:640], a[655:648], a[663:656], a[679:672], a[687:680], a[695:688], a[703:696], a[711:704], a[719:712], a[727:720], a[735:728], a[743:736], a[751:744], a[767:760], a[775:768], a[783:776], a[791:784], a[799:792], a[807:800], a[815:808], a[823:816], a[831:824], a[839:832], a[855:848], a[863:856], a[871:864], a[879:872], a[887:880], a[895:888], a[903:896], a[911:904], a[919:912], a[927:920], a[943:936], a[951:944], a[959:952], a[967:960]}, w6);
matdet10 md7({a[95:88], a[103:96], a[111:104], a[119:112], a[127:120], a[135:128], a[143:136], a[159:152], a[167:160], a[175:168], a[183:176], a[191:184], a[199:192], a[207:200], a[215:208], a[223:216], a[231:224], a[247:240], a[255:248], a[263:256], a[271:264], a[279:272], a[287:280], a[295:288], a[303:296], a[311:304], a[319:312], a[335:328], a[343:336], a[351:344], a[359:352], a[367:360], a[375:368], a[383:376], a[391:384], a[399:392], a[407:400], a[423:416], a[431:424], a[439:432], a[447:440], a[455:448], a[463:456], a[471:464], a[479:472], a[487:480], a[495:488], a[511:504], a[519:512], a[527:520], a[535:528], a[543:536], a[551:544], a[559:552], a[567:560], a[575:568], a[583:576], a[599:592], a[607:600], a[615:608], a[623:616], a[631:624], a[639:632], a[647:640], a[655:648], a[663:656], a[671:664], a[687:680], a[695:688], a[703:696], a[711:704], a[719:712], a[727:720], a[735:728], a[743:736], a[751:744], a[759:752], a[775:768], a[783:776], a[791:784], a[799:792], a[807:800], a[815:808], a[823:816], a[831:824], a[839:832], a[847:840], a[863:856], a[871:864], a[879:872], a[887:880], a[895:888], a[903:896], a[911:904], a[919:912], a[927:920], a[935:928], a[951:944], a[959:952], a[967:960]}, w7);
matdet10 md8({a[95:88], a[103:96], a[111:104], a[119:112], a[127:120], a[135:128], a[143:136], a[151:144], a[167:160], a[175:168], a[183:176], a[191:184], a[199:192], a[207:200], a[215:208], a[223:216], a[231:224], a[239:232], a[255:248], a[263:256], a[271:264], a[279:272], a[287:280], a[295:288], a[303:296], a[311:304], a[319:312], a[327:320], a[343:336], a[351:344], a[359:352], a[367:360], a[375:368], a[383:376], a[391:384], a[399:392], a[407:400], a[415:408], a[431:424], a[439:432], a[447:440], a[455:448], a[463:456], a[471:464], a[479:472], a[487:480], a[495:488], a[503:496], a[519:512], a[527:520], a[535:528], a[543:536], a[551:544], a[559:552], a[567:560], a[575:568], a[583:576], a[591:584], a[607:600], a[615:608], a[623:616], a[631:624], a[639:632], a[647:640], a[655:648], a[663:656], a[671:664], a[679:672], a[695:688], a[703:696], a[711:704], a[719:712], a[727:720], a[735:728], a[743:736], a[751:744], a[759:752], a[767:760], a[783:776], a[791:784], a[799:792], a[807:800], a[815:808], a[823:816], a[831:824], a[839:832], a[847:840], a[855:848], a[871:864], a[879:872], a[887:880], a[895:888], a[903:896], a[911:904], a[919:912], a[927:920], a[935:928], a[943:936], a[959:952], a[967:960]}, w8);
matdet10 md9({a[95:88], a[103:96], a[111:104], a[119:112], a[127:120], a[135:128], a[143:136], a[151:144], a[159:152], a[175:168], a[183:176], a[191:184], a[199:192], a[207:200], a[215:208], a[223:216], a[231:224], a[239:232], a[247:240], a[263:256], a[271:264], a[279:272], a[287:280], a[295:288], a[303:296], a[311:304], a[319:312], a[327:320], a[335:328], a[351:344], a[359:352], a[367:360], a[375:368], a[383:376], a[391:384], a[399:392], a[407:400], a[415:408], a[423:416], a[439:432], a[447:440], a[455:448], a[463:456], a[471:464], a[479:472], a[487:480], a[495:488], a[503:496], a[511:504], a[527:520], a[535:528], a[543:536], a[551:544], a[559:552], a[567:560], a[575:568], a[583:576], a[591:584], a[599:592], a[615:608], a[623:616], a[631:624], a[639:632], a[647:640], a[655:648], a[663:656], a[671:664], a[679:672], a[687:680], a[703:696], a[711:704], a[719:712], a[727:720], a[735:728], a[743:736], a[751:744], a[759:752], a[767:760], a[775:768], a[791:784], a[799:792], a[807:800], a[815:808], a[823:816], a[831:824], a[839:832], a[847:840], a[855:848], a[863:856], a[879:872], a[887:880], a[895:888], a[903:896], a[911:904], a[919:912], a[927:920], a[935:928], a[943:936], a[951:944], a[967:960]}, w9);
matdet10 md10({a[95:88], a[103:96], a[111:104], a[119:112], a[127:120], a[135:128], a[143:136], a[151:144], a[159:152], a[167:160], a[183:176], a[191:184], a[199:192], a[207:200], a[215:208], a[223:216], a[231:224], a[239:232], a[247:240], a[255:248], a[271:264], a[279:272], a[287:280], a[295:288], a[303:296], a[311:304], a[319:312], a[327:320], a[335:328], a[343:336], a[359:352], a[367:360], a[375:368], a[383:376], a[391:384], a[399:392], a[407:400], a[415:408], a[423:416], a[431:424], a[447:440], a[455:448], a[463:456], a[471:464], a[479:472], a[487:480], a[495:488], a[503:496], a[511:504], a[519:512], a[535:528], a[543:536], a[551:544], a[559:552], a[567:560], a[575:568], a[583:576], a[591:584], a[599:592], a[607:600], a[623:616], a[631:624], a[639:632], a[647:640], a[655:648], a[663:656], a[671:664], a[679:672], a[687:680], a[695:688], a[711:704], a[719:712], a[727:720], a[735:728], a[743:736], a[751:744], a[759:752], a[767:760], a[775:768], a[783:776], a[799:792], a[807:800], a[815:808], a[823:816], a[831:824], a[839:832], a[847:840], a[855:848], a[863:856], a[871:864], a[887:880], a[895:888], a[903:896], a[911:904], a[919:912], a[927:920], a[935:928], a[943:936], a[951:944], a[959:952]}, w10);
mul m0(a[7:0], w0, w11);
mul m1(a[15:8], w1, w12);
mul m2(a[23:16], w2, w13);
mul m3(a[31:24], w3, w14);
mul m4(a[39:32], w4, w15);
mul m5(a[47:40], w5, w16);
mul m6(a[55:48], w6, w17);
mul m7(a[63:56], w7, w18);
mul m8(a[71:64], w8, w19);
mul m9(a[79:72], w9, w20);
mul m10(a[87:80], w10, w21);
sub op0(w11, w12, w22);
add op1(w22, w13, w23);
sub op2(w23, w14, w24);
add op3(w24, w15, w25);
sub op4(w25, w16, w26);
add op5(w26, w17, w27);
sub op6(w27, w18, w28);
add op7(w28, w19, w29);
sub op8(w29, w20, w30);
add op9(w30, w21, det);
endmodule
