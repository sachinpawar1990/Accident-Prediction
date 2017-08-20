# Code to create the PNN model and make predictions
library(pnn)

# Reading the training data
all_data <- read.csv("C://AccVehBrkDown_Speedbands_2.csv")
all_data <- all_data[,1:10]

# Learning the PNN model
pnn <- learn(all_data)
pnn <- smooth(pnn, sigma=0.5)

prob_0 = {}
prob_1 = {}

for (i in 1:dim(all_data)[1]){
  
  cur_slat = all_data[i,2]
  cur_slon = all_data[i,3]
  cur_sb = all_data[i,4]
  cur_hr = all_data[i,5]
  cur_min = all_data[i,6]
  cur_wea = all_data[i,7]
  cur_elat = all_data[i,8]
  cur_elon = all_data[i,9]
  cur_day = all_data[i,10]
  
  # Making predictions  
  prob_0[i] = guess(pnn,c(cur_slat,cur_slon,cur_sb,cur_hr,cur_min,cur_wea,cur_elat,cur_elon,cur_day))$probabilities[1]
  prob_1[i] = guess(pnn,c(cur_slat,cur_slon,cur_sb,cur_hr,cur_min,cur_wea,cur_elat,cur_elon,cur_day))$probabilities[2]
  
  next
}

# Writing the made predictions to a csv file
x <- data.frame(prob_0, prob_1)
write.table(x, file = 'C://Probs_0_1.csv', row.names=FALSE,col.names=FALSE)