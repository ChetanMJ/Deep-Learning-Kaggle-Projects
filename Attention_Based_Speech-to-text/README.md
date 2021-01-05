## kaggle link:
https://www.kaggle.com/c/11785-fall19-hw4p2

Also refer the details in the attached pdf doc

## Approach:
Encoder: used 3 layer PBLSTM and a biLSTM as initial layer with 256 hidden size in each direction. Also added 3 dropout layers with probability of 0.2, one each for the output of pibilstm
Attention: Used the exact aproach mentioned in recitions
Decoder: used 2 lstm cells with attentions with 512 hidden size. Also, used drop out layer with probability of 0.2 for output of each lstm cell.
Batchsize: 128
Initialise: Xavier initialization
Decoding: Greedy search
No. of epochs: 22nd epochs or 21st epoch number as in log (even though i ran until 26 epochs, I had to search for the best one among the outputs for each epoch starting 20)
Teacher forcing and Gumble noise: TF and GN was avoided for initial character input to decoder while training as it going to remain same even during testing
                                  TF rate started with 0.1 and gradually increased by 5% in every subsequebt epoch until it reached a max of 0.4
Also during testing, index of '<sos>' was passed as first character. This made a difference as well
Index handling: each character index was incremented by 1 during letter to index transformation and mask indexes were handled accordingly. This made hude difference in final output.

Other aproaches which were close but not enough: batchsize - 64, 2 dropouts in encoder and 1 in decoder with 0.1 prob until epoch 29 
                                                 and increase drop out to 0.2 unntil epoch 50. With rest of the remain same as above. 
                                                 Although, loss was lower, but this took me only upto score of 12.8 which means it was overfitting. 
                                                 So, batch size increase from 64 to 128 was and dropout porb increase from start to 0.2 was helpfull.
