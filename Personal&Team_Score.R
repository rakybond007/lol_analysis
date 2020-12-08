personal_transfer_result <- read.csv('./18_19_Personal&Team_Score.csv', header=T)
personal_transfer_result2 <- read.csv('./20_Personal&Team_Score.csv', header=T)
sub_ptr <-  personal_transfer_result[,-c(1,2,6,7)]

sub_ptrs <- scale(sub_ptr)

library(psych)
scree(sub_ptrs, factors=FALSE, pc=TRUE)
pcav <- principal(sub_ptrs, nfactors=2, rotate='varimax')
pcav

sub_ptr2 <-  personal_transfer_result[,-c(1,2,3,4,5)]

sub_ptrs2 <- scale(sub_ptr2)

library(psych)
scree(sub_ptrs2, factors=FALSE, pc=TRUE)
pcav2 <- principal(sub_ptrs2, nfactors=1, rotate='varimax')
pcav2

gg <- glm.fit(Transfer~KDA+WR+KPAR+Team.Rank+Team.Pts, family=binomial(logit),data=personal_transfer_result)
summary(gg)

p <- predict(gg.fit, personal_transfer_result2)
pr <- 1/(1+exp(-p))
pr2 <- ifelse(pr > 0.5, "0", "1")
pr3 <- ifelse(p > 0.5, "0", "1")

predict_result <- data.frame(personal_transfer_result2$Player, as.vector(pr2))

write.csv(predict_result, "./transfer_predict.csv")
