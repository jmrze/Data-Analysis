## R Markdown

This is an R Markdown document. Markdown is a simple formatting syntax for authoring HTML, PDF, and MS Word documents. For more details on using R Markdown see <http://rmarkdown.rstudio.com>.

When you click the **Knit** button a document will be generated that includes both content as well as the output of any embedded R code chunks within the document. You can embed an R code chunk like this:

```{r cars}
summary(cars)
```

## Including Plots

You can also embed plots, for example:

```{r pressure, echo=FALSE}
plot(pressure)
```

Note that the `echo = FALSE` parameter was added to the code chunk to prevent printing of the R code that generated the plot.

# Preamble

packages, wd, colours

```{r preamble}
rm(list = ls())

library(tidyverse)
library(MASS)
library(fitdistrplus)
library(nortest)
library(survival)
library(RColorBrewer)
library(wesanderson)
library(ggsci)
library(ggfortify)
library(lmtest)
library(ggpointdensity)
library(lubridate)
library(ggpubr)
library(ggExtra)
library(gridExtra)

# wd for university and home PC respectively
#setwd("M:\\L5\\Stats\\ClassReport\\Oct 24 mice ageing\\Data")
setwd("C:\\Users\\jamie\\OneDrive - University of Glasgow\\Year 5\\Stats\\report\\Oct 24 mice ageing\\dataset\\Data")

# reset for "Error in .Call.graphics(C_palette2, .Call(C_palette2, NULL)) : invalid graphics state"
#dev.off()

dietcolours <- RColorBrewer::brewer.pal("Dark2", n = 5)[1:5]
    #wes_palette("AsteroidCity2")[1:5]


#dietcolours <- c("lightgrey", "chartreuse2", "indianred1", "slateblue3", #"gold2")
dietnames <- c("AL", "1D", "2D", "20", "40")
names(dietcolours) <- dietnames
```

# Data Manipulation

Loading survival, bw, food dfs, summary stats, merging dfs

```{r microbiome data}
# microbiome <- read.csv("Microbiome\\all_genus_features_clr_n2997x107_230626.csv")
# 
# tibble(microbiome)

```

```{r survival data}
survival <- read.csv("Animal\\AnimalData_Processed_20230712.csv",
                       stringsAsFactors = TRUE) %>% 
  filter(SurvDays > 179) %>% 
  mutate(Diet = factor(Diet, levels = dietnames)) 
  # trial started at 6 months age, filter for age > 179

glimpse(survival)
summary(survival)

# summary stats per diet group
survival_avg <- survival %>% 
                  group_by(Diet) %>% 
                    summarise(mean_survival = mean(SurvDays),
                              sd_survival = sd(SurvDays),
                              se_survival = sd(SurvDays)/sqrt(n()),
                              ci_survival_lower = mean(SurvDays) - 1.96 * se_survival,
                              ci_survival_upper = mean(SurvDays) + 1.96 * se_survival)

glimpse(survival_avg)

survival %>% 
  group_by(Diet) %>% 
    count()
```

```{r bodyweight data}
bodyweight <- read.csv("BW\\WeeklyBW_Processed_20230712.csv",
                       stringsAsFactors = TRUE)

glimpse(bodyweight)

bodyweight_avg  <- bodyweight %>% 
                       group_by(MouseID) %>% 
                       summarise(mean_bw = mean(BW_Raw),
                                 sd_bw = sd(BW_Raw),
                                 se_bw = sd(BW_Raw)/sqrt(n()),
                                 ci_bw_upper = mean_bw + 1.96*se_bw,
                                 ci_bw_lower = mean_bw - 1.96*se_bw)

glimpse(bodyweight_avg)
```

```{r food data}
# food <- read.csv("Cross_Sectional\\FoodConsumption_20221017.csv")
# 
# food_avg <- food %>% 
#   group_by(Diet) %>% 
#   summarise(mean_calorie = mean(FoodConsumedPerMouse),
#             sd_calorie = sd(FoodConsumedPerMouse),
#             se_calorie = sd(FoodConsumedPerMouse)/sqrt(n()),
#             ci_calorie_upper = mean_calorie + 1.96*se_calorie,
#             ci_calorie_lower = mean_calorie - 1.96*se_calorie)
# 
# food
# 
# nmr <- read.csv("Cross_Sectional\\NMR_20230420.csv")
# 
# tibble(food)
# 
# tibble(nmr)

```

```{r bodyweight distribution}
# distribution of body weights - is the mean bw normally distributed? ####
# hist(bodyweight$BW_Raw, breaks = 50)
#   ad.test(x = bodyweight$BW_Raw) # p < 2.2e-16 i.e not normal
#   
# fitN <-   fitdistr(x = bodyweight$BW_Raw,densfun = "normal")
#   fitN <- fitdist(bodyweight$BW_Raw, "norm")
#   summary(fitN)
# 
#   plotdist(bodyweight$BW_Raw, 
#            "norm", 
#            para = list(
#              mean = fitN$estimate[1],
#              sd = fitN$estimate[2]))
#   
# gofstat(fitN, 
#         fitnames = "normal")
# 
# ks.test(bodyweight$BW_Raw, y = "pnorm", mean = 32.1)
# 
# mean(bodyweight$BW_Raw)
# 
#           hist(bodyweight_avg$mean_bw, breaks = 50)
# shapiro.test(x = bodyweight_avg$mean_bw) # W = 0.978, p < 8.5e-11 i.e normally distributed
```

```{r merge dfs}

survival_bodyweight_avg <- merge(bodyweight_avg, survival, by = "MouseID")

bodyweight_diet_avg <- survival_bodyweight_avg %>% 
                          group_by(Diet) %>% 
                            summarise(mean_bw_diet = mean(mean_bw),
                                      sd_bw_diet = sd(mean_bw),
                                      se_bw_diet = sd(mean_bw)/sqrt(n()),
                                      ci_bw_diet_upper = mean_bw_diet + 1.96*se_bw_diet,
                                      ci_bw_diet_lower = mean_bw_diet - 1.96*se_bw_diet)

survival_avg_bodyweight_avg <- merge(survival_avg, bodyweight_diet_avg, by = "Diet")

#survival_avg_bodyweight_avg_food_avg <- merge(survival_avg_bodyweight_avg, food_avg, by = "Diet")
```

# Summary Statistics

```{r stats}
mean(survival$SurvDays)

median(survival$SurvDays)

survival %>% 
  group_by(Diet) %>% 
  summarise(mean = mean(SurvDays),
            median = median(SurvDays),
            sd = sd(SurvDays),
            se = sd(SurvDays)/sqrt(n()),
            num = n(),
            max = max(SurvDays),
            min = min(SurvDays))

survival_bodyweight_avg %>% 
  group_by(Diet) %>% 
  summarise(mean = mean(mean_bw),
            median = median(mean_bw),
            sd = sd(mean_bw),
            se = sd(mean_bw)/sqrt(n()),
            num = n(),
            max = max(mean_bw),
            min = min(mean_bw))

ALvs40 <- subset(survival, Diet %in% c("AL", "40"))
  t.test(data = subset, SurvDays~Diet)

ALvs20 <- subset(survival, Diet %in% c("AL", "20"))
  t.test(data = ALvs20, SurvDays~Diet)

t.test(SurvDays~Diet, data = survival, formula = )
print(cor(survival_bodyweight_avg$mean_bw, survival_bodyweight_avg$SurvDays))

TukeyHSD(aov(model_survival_diet))

glm1 <- glm(data = survival, SurvDays ~ Diet, family = "gaussian")

summary(glm1)
anova(glm1)
```

# Plots

ggplot visualisations of different explanatory/response variables

```{r figure 1 - survival vs diet}

theme_set(new = theme_light())

#### survival vs. diet ####

#### dotplot of mean survival by diet, SEM as error bars ####
plot1 <- survival_avg_bodyweight_avg %>% 
  ggplot(aes(x = Diet,
             y = mean_survival,
             colour = Diet)) +
  geom_point(cex = 5) +
  geom_errorbar(
    # aes(ymin = mean_survival - 1.96*se_survival,
    #     ymax = mean_survival + 1.96*se_survival,
    aes(ymin = ci_survival_lower,
        ymax = ci_survival_upper),
    linewidth = 1,
    width = 0.5) +
  coord_flip() +
  labs(title = "Mean Lifespan vs Diet",
       x = "Diet",
       y = "Mean Lifespan (days)") +
  scale_colour_manual(values = dietcolours,
                      labels = dietnames) + theme_light(base_size = 14) +
  theme(legend.position = "none")
  #scale_colour_brewer("Dark2", n = 5, aesthetics = dietnames)
                   #labels = dietnames)
  plot1
  #ggsave("lifespan_vs_diet_dotplot.svg", width = 7, height = 5, dpi = 1200)

#### boxplot of mean survival by diet ####
plot2 <- survival %>% 
  ggplot(aes(x = Diet,
             y = SurvDays,
             colour = Diet,
             legend(dietnames))
         ) +
  geom_boxplot(size = 1) +
  geom_jitter(aes(alpha = 0.5), size = 1.5, width = 0.3) +
  #geom_point(aes(alpha = 0.1)) +
  #scale_color_brewer(palette = "Dark2", n = 5, aesthetics = dietnames)
  scale_colour_manual(values = dietcolours,
                      labels = dietnames) +
   labs(x = "Diet",
       y = "Lifespan (days)",
       title = "Lifespan vs. Diet") +      theme_light(base_size = 14) + 
    theme(legend.position = "none") + 
    coord_flip()

  # save plot 1 and 2
  plot2
  ggarrange(plot1, plot2, legend = "none", widths = 5, heights = 5, labels = c("A","B"), font.label = list(size = 20))
  ggsave("fig1_2.png", width = 10, height = 5)
  ggsave("fig.1_3.png", dpi=300, height=5, width=10, units="in")
```

```{r figure 2 bodyweight vs diet}
plot3 <- survival_avg_bodyweight_avg %>% 
  ggplot(aes(x = Diet,
             y = mean_bw_diet,
             colour = Diet)) +
  geom_point(cex = 5,
             alpha = 1) +
  geom_errorbar(
    aes(ymin = ci_bw_diet_lower,
        ymax = ci_bw_diet_upper),
    linewidth = 1,
    width = 0.5) +
  labs(title = "Mean Lifetime Body Weight vs Diet",
       x = "Diet",
       y = "Mean Lifetime Body Weight (g)") +
  scale_colour_manual(values = dietcolours,
                      labels = dietnames) + theme_light(base_size = 14) +
  theme(legend.position = "none")

plot3
#### boxplot of mean body weight by diet ####
plot4 <- survival_bodyweight_avg %>% 
  ggplot(aes(x = Diet,
             y = mean_bw,
             colour = Diet)
         ) +
  geom_boxplot(size = 1) +
  geom_jitter(aes(alpha = 0.1), size = 1.5, width = 0.4) +
  #geom_point(aes(alpha = 0.1)) +
  #scale_color_brewer(palette = "Dark2"[1:5], n = 5, aesthetics = dietnames)
  scale_colour_manual(values = dietcolours,
  labels = dietnames) +
   labs(x = "Diet",
        y = "Mean Lifetime Body Weight (g)",
        title = "Mean Lifetime Body Weight vs. Diet") +
  theme_light(base_size = 14) + theme(legend.position = "none")
  


plot4

ggarrange(plot3, plot4, legend = "none", widths = 5, heights = 5, labels = c("A","B"), font.label = list(size = 20))
ggsave("fig2_2.png", width = 10, height = 5)
ggsave("fig.2_3.png", dpi=300, height=5, width=10, units="in")
```

```{r figure 3 survival vs bodyweight vs diet}
#### scatterplot of mean survival vs mean body weight with 95% CIs ####
plot5 <- survival_avg_bodyweight_avg %>% 
  ggplot(aes(x = mean_bw_diet,
             y = mean_survival,
             colour = Diet)) +
  geom_point(cex = 4,
             alpha = 1) +
  geom_errorbar(aes(ymax = ci_survival_upper,
                    ymin = ci_survival_lower), 
                linewidth = 1,
                width = 0.5
                ) +
  geom_errorbarh(aes(xmax = ci_bw_diet_upper,
                     xmin = ci_bw_diet_lower), 
                 linewidth = 1,
                 width = 0.5
                 ) +
  labs(title = "Mean Lifespan vs Mean Body Weight",
       subtitle = "by Diet",
       x = "Mean Lifetime Body Weight (g)",
       y = "Mean Lifespan (days)") +
  scale_colour_manual(values = dietcolours,
                      labels = dietnames) + theme_light(base_size = 14)
  #scale_colour_brewer("Dark2", n = 5, aesthetics = dietnames)
plot5

#### scatterplot of survival vs mean body weight (n = 937) #####
plot6 <- survival_bodyweight_avg %>% 
  # mutate(cat_bw = cut(SurvDays,
  #   breaks = 4,
  #   labels = c("Q1", "Q2", "Q3", "Q4")
  # )) %>%
  ggplot(aes(x = mean_bw,
             y = SurvDays,
             colour = Diet)) +
  geom_point(pch = 19,
             cex = 2,
             alpha = 0.75,
             aes(colour = Diet)) +
  labs(title = "Lifespan vs. Mean Body Weight",
       subtitle = "By Diet",
       x = "Mean Lifetime Body Weight (g)",
       y = "Lifespan (days)") +
  scale_colour_manual(values = dietcolours,
                      labels = dietnames) + theme_light(base_size = 14) #+
 #facet_wrap(survival_bodyweight_avg$Diet)
  
  plot6
  marginal<- ggMarginal(p = plot6, type="boxplot")
  marginal
  #ggsave("mousesurvival_vs_meanbodyweight_scatterplot.svg", height = 5, width = 7, dpi = 1200) 
  
  ggarrange(plot5, plot6, common.legend = T, legend = "bottom", heights = 5, widths = 5, labels = c("A","B"), font.label = list(size = 20))
  
  ggsave("fig3_2.png", width = 10, height = 6)
  ggsave("fig.3_4.png", dpi=300, height=5.5, width=10, units="in")
  
  # geom_jitter(width = 1,
  #             alpha = 0.5,
  #             aes(colour = Diet)) #+
  #facet_wrap(~Diet)
  #scale_color_brewer(palette = "Dark2", n = 5, aesthetics = dietnames)
```

```{r lollipop charts - z-score normalised survival and weight deviations}
##### Lollipop chart - z-score bw by diet ####

plot7 <- survival_avg_bodyweight_avg %>%
  mutate(
    allmeanbw = mean(mean_bw_diet),
    allsdbw = sd(mean_bw_diet),
    zscore = ((mean_bw_diet - allmeanbw)/allsdbw)
    ) %>% 
  ggplot(aes(x = Diet,
             y = zscore, 
             colour = Diet)) +
  geom_segment(aes(x = Diet,
                   xend = Diet,
                   y = 0,
                   yend = zscore),
               colour = "grey",
               linewidth = 1) +
  geom_point(size = 5,
             aes(colour = Diet)) +
  theme(
    panel.grid.major.x = element_blank(),
    panel.border = element_blank(),
    axis.ticks.x = element_blank()) +
  scale_colour_manual(values = dietcolours,
                      labels = dietnames) +
  labs(title = "Z-score Normalised Deviation of Mean Lifetime Body Weight",
       subtitle = "By Diet",
       x = "Diet",
       y = "Z-score")

##### Lollipop chart - z-score lifespan by diet #####
plot8 <- survival_avg_bodyweight_avg %>%
  mutate(
    allmean = mean(mean_survival),
    allsd = sd(mean_survival),
    zscore = ((mean_survival - allmean)/allsd)
    ) %>% 
  ggplot(aes(x = Diet,
             y = zscore, 
             colour = Diet)) +
  geom_segment(aes(x = Diet,
                   xend = Diet,
                   y = 0,
                   yend = zscore),
               colour = "grey",
               linewidth = 1) +
  geom_point(size = 5,
             aes(colour = Diet)) +
  theme(
    panel.grid.major.x = element_blank(),
    panel.border = element_blank(),
    axis.ticks.x = element_blank()) +
  scale_colour_manual(values = dietcolours,
                      labels = dietnames) +
  labs(title = "Z-score Normalised Deviation of Mean Lifespan by Diet",
       x = "Diet",
       y = "Z-score")

 ggarrange(plot7, plot8, legend = "none", widths = 5, heights = 5, labels = c("A","B"), font.label = list(size = 20), align = "hv")
 ggsave("fig4.png", width = 10, height = 5)

```

# GLMs

-   survival\~diet

-   survival\~mean body weight

-   survival\~diet+mean body weight

-   survival\~diet\*mean body weight

-   body weight\~diet

-   food consumption\~diet

-   mean survival\~food consumption

```{r glm survival ~ diet}
model_survival_diet <- lm(SurvDays~Diet, data = survival)
summary(model_survival_diet)
anova(model_survival_diet)#

autoplot(model_survival_diet)

plot(model_survival_diet)

png("lifespan~diet.png", width = 10, height = 10, units = "in", res = 300)

par(mfrow=c(2,2))

plot(model_survival_diet)

dev.off()
```

```{r glm survival ~ mean body weight}
## survival ~ mean body weight
model_survival_meanbw <- lm(SurvDays~mean_bw, data = survival_bodyweight_avg)
summary(model_survival_meanbw)
anova(model_survival_meanbw)
autoplot(model_survival_meanbw, main = "survival vs bw")
  # 1 = no underlying pattern
  # 2 = approx normal residuals
  # 3 = heteroscadiscity
  # 4 = 
  bptest(model_survival_meanbw) # p < 2e-13 i.e heteroskedasticity
  
png("lifespan~bw.png", width = 10, height = 10, units = "in", res = 300)

par(mfrow=c(2,2))

plot(model_survival_meanbw)

dev.off()
```

```{r glm survival ~ diet + mean body weight}
model_survival_diet_meanbw <- lm(SurvDays~Diet+mean_bw, data = survival_bodyweight_avg)
summary(model_survival_diet_meanbw)
anova(model_survival_diet_meanbw)

plot_diet_plus_bw <- autoplot(model_survival_diet__meanbw)

png("diet_plus_bw.png", width = 10, height = 10, units = "in", res = 300)

par(mfrow=c(2,2))

plot(model_survival_diet_meanbw)

dev.off()

ggsave("survival_diet_+_meanbw_plot.png", dpi = 300, width = 10, height = 10, plot = PLOT_survivaldiet_plus_meanbw)
```

```{r glm survival ~ diet * mean body weight i.e interaction}
model_survival_diet_x_meanbw <- lm(SurvDays~Diet*mean_bw, data = survival_bodyweight_avg)
summary(model_survival_diet_x_meanbw)
anova(model_survival_diet_x_meanbw)

# plotting - open graphic device, arrange grid, device off
plot_diet_times_bw <- autoplot(model_survival_diet_x_meanbw)

png("diet_times_bw.png", width = 10, height = 10, units = "in", res = 300)

par(mfrow=c(2,2))

plot(model_survival_diet_x_meanbw)

dev.off()

#ggsave("diet_times_bw.png", plot = plot_diet_times_bw, width = 10, height = 10)

```

```{r glm body weight ~ diet}
model_meanbw_diet <- lm(mean_bw ~ Diet, data = survival_bodyweight_avg)
summary(model_meanbw_diet)
anova(model_meanbw_diet)

autoplot(model_meanbw_diet)
plot(model_meanbw_diet)

#   #hist(model_meanbw_diet$residuals)
```

# Model Evaluation

```{r LRT - LogLik AIC etc - model selection}

# LRT interaction vs addition model

logLik(model_survival_diet_x_meanbw) # 'log Lik.' -6577.173 (df=11)

logLik(model_survival_diet_meanbw) # 'log Lik.' -6578.477 (df=7)

two_delta_LL_1 <- 2*(-6577.173 - (-6578.477)) # 2.608

1 - pchisq(2.608, 4) # p = 0.625 i.e reject alternative hypothesis, accept null
  # thus adopt the simpler additive model: model_survival_diet_meanbw

# LRT additive model vs single varialbe models 

logLik(model_survival_meanbw) # 'log Lik.' -6607.546 (df=3)

  two_delta_LL_2 <- 2*(-6578.477 - (-6607.546)) # 58.13

  1 - pchisq(58.138, 4) # p = 7.138e-12 i.e accept alternate hypothesis
  # thus adopt more complex model: model_survival_diet_meanbw

logLik(model_survival_diet) # 'log Lik.' -6578.968 (df=6)

  two_delta_LL_3 <- 2*(-6578.477 - (-6578.968)) # 0.982
  
  1 - pchisq(0.982, 1) # p = 0.321 i.e reject alternate hypothesis
  # thus adopt more complex model: model_survival_diet_meanbw

1 - pchisq(2*(-6577.173 - (-6578.968)), 5)

```

```{r model diagnostics}
#### survival ~ mean_BW ####
autoplot(model_survival_meanbw, main = "survival vs bw")
  # 1 = no underlying pattern
  # 2 = approx normal residuals
  # 3 = heteroscadiscity
  # 4 = 
  bptest(model_survival_meanbw) # p < 2e-13 i.e heteroskedasticity
  plot(model_survival_meanbw,which=4)
  
#### survival ~ diet ####
  autoplot(model_survival_diet)
    plot(model_survival_diet,which=4)
    
#### survival ~ diet + mean body weight ####
  autoplot(model_survival_diet_meanbw)
    
#### survival ~ diet * mean body weight ####
  autoplot(model_survival_diet_x_meanbw)
    
#### body weight ~ diet ####
    autoplot(model_meanbw_diet)
    
#### food ~ diet ####
  autoplot(model_food_diet)
    # bad model
    
#### survival ~ food ####
  autoplot(model_survival_food)
    # bad model
```
