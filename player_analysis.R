# avg
avg1819 <- read.csv("./parse/18-to-19-avg.csv", header=T)
avg1920 <- read.csv("./parse/19-to-20-avg.csv", header=T)

# 1819
avg1819_t <- avg1819[avg1819$Transfer==1,]
avg1819_nt <- avg1819[avg1819$Transfer==0,]

var.test(avg1819_t$dt.WR., avg1819_nt$dt.WR.)

t.test(avg1819_t$dt.WR., avg1819_nt$dt.WR., var.equal=T)

# 1920
avg1920_t <- avg1920[avg1920$Transfer==1,]
avg1920_nt <- avg1920[avg1920$Transfer==0,]

var.test(avg1920_t$dt.WR., avg1920_nt$dt.WR.)

t.test(avg1920_t$dt.WR., avg1920_nt$dt.WR., var.equal=T)

# 181920
avg181920_t <- rbind(avg1819_t, avg1920_t)
avg181920_nt <- rbind(avg1819_nt, avg1920_nt)

var.test(avg181920_t$dt.WR., avg181920_nt$dt.WR.)

t.test(avg181920_t$dt.WR., avg181920_nt$dt.WR., var.equal=T)

# ratio
ratio1819 <- read.csv("./parse/18-to-19-ratio.csv", header=T)
ratio1920 <- read.csv("./parse/19-to-20-ratio.csv", header=T)

# 1819
ratio1819_t <- ratio1819[ratio1819$Transfer==1,]
ratio1819_nt <- ratio1819[ratio1819$Transfer==0,]

ratio1819_nt_14 <- ratio1819_nt[sample(nrow(ratio1819_nt), 14),]

var.test(ratio1819_t$dt.WR., ratio1819_nt_14$dt.WR.)

t.test(ratio1819_t$dt.WR., ratio1819_nt_14$dt.WR., var.equal=T)

mean(avg1819_t$dt.WR.)
mean(avg1819_nt$dt.WR.)
mean(ratio1819_nt$dt.WR.)
mean(ratio1819_t$dt.WR.)

