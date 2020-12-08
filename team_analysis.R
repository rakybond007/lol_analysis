team_result <- read.csv('./roster_result2.csv', header=T)

##### Top change #####
team_result_tc <- team_result[team_result$Top==1,]
team_result_tnc <- team_result[team_result$Top==0,]

var.test(team_result_tc$dt.RANK., team_result_tnc$dt.RANK.)

t.test(team_result_tc$dt.RANK., team_result_tnc$dt.RANK., var.equal=T)

## RESULT: Top change, rank up

##### Jungle change #####
team_result_jc <- team_result[team_result$Jungle==1,]
team_result_jnc <- team_result[team_result$Jungle==0,]

var.test(team_result_jc$dt.RANK., team_result_jnc$dt.RANK.)

t.test(team_result_jc$dt.RANK., team_result_jnc$dt.RANK., var.equal=T)

## RESULT: Jungle change, rank down

##### Mid change #####
team_result_mc <- team_result[team_result$Mid==1,]
team_result_mnc <- team_result[team_result$Mid==0,]

var.test(team_result_mc$dt.RANK., team_result_mnc$dt.RANK.)

t.test(team_result_mc$dt.RANK., team_result_mnc$dt.RANK., var.equal=F)

## RESULT: Mid change, rank down

##### Bot change #####
team_result_bc <- team_result[team_result$Bot==1,]
team_result_bnc <- team_result[team_result$Bot==0,]

var.test(team_result_bc$dt.RANK., team_result_bnc$dt.RANK.)

t.test(team_result_bc$dt.RANK., team_result_bnc$dt.RANK., var.equal=T)

## RESULT: Bot change, rank up, smaller than mid, jungle, top

##### Support change #####
team_result_sc <- team_result[team_result$Support==1,]
team_result_snc <- team_result[team_result$Support==0,]

var.test(team_result_sc$dt.RANK., team_result_snc$dt.RANK.)

t.test(team_result_sc$dt.RANK., team_result_snc$dt.RANK., var.equal=F)

## RESULT: Support change, rank up, too small

##### Bot Support Duo change #####
team_result_bsc <- team_result[team_result$Support==1,]
team_result_bsc <- team_result_bsc[team_result_bsc$Bot==1,]
team_result_bsnc <- team_result[team_result$Support==0,]
team_result_bsnc <- team_result_bsnc[team_result_bsnc$Bot==0,]

var.test(team_result_bsc$dt.RANK., team_result_bsnc$dt.RANK.)

t.test(team_result_bsc$dt.RANK., team_result_bsnc$dt.RANK., var.equal=F)

## RESULT: Bot, Support change, rank up, too small

##### Jungle Mid change #####
team_result_jmc <- team_result[team_result$Mid==1,]
team_result_jmc <- team_result_jmc[team_result_jmc$Jungle==1,]
team_result_jmnc <- team_result[team_result$Mid==0,]
team_result_jmnc <- team_result_jmnc[team_result_jmnc$Jungle==0,]

var.test(team_result_jmc$dt.RANK., team_result_jmnc$dt.RANK.)

t.test(team_result_jmc$dt.RANK., team_result_jmnc$dt.RANK., var.equal=T)

## RESULT: Jungle Mid change, rank down a little, not change, rank 0.8 up

##### Top Jungle change #####
team_result_tjc <- team_result[team_result$Top==1,]
team_result_tjc <- team_result_tjc[team_result_tjc$Jungle==1,]
team_result_tjnc <- team_result[team_result$Top==0,]
team_result_tjnc <- team_result_tjnc[team_result_tjnc$Jungle==0,]

var.test(team_result_tjc$dt.RANK., team_result_tjnc$dt.RANK.)

t.test(team_result_tjc$dt.RANK., team_result_tjnc$dt.RANK., var.equal=T)

## RESULT: Jungle Mid change, rank up, not change, rank up ???

##### Top Jungle mid change #####
team_result_tjmc <- team_result[team_result$Top==1,]
team_result_tjmc <- team_result_tjc[team_result_tjc$Jungle==1,]
team_result_tjmc <- team_result_tjc[team_result_tjc$Mid==1,]
team_result_tjmnc <- team_result[team_result$Top==0,]
team_result_tjmnc <- team_result_tjnc[team_result_tjnc$Jungle==0,]
team_result_tjmnc <- team_result_tjnc[team_result_tjnc$Mid==0,]

var.test(team_result_tjmc$dt.RANK., team_result_tjmnc$dt.RANK.)

t.test(team_result_tjmc$dt.RANK., team_result_tjmnc$dt.RANK., var.equal=T)

## RESULT: Jungle Mid change, rank up, not change, rank up ???