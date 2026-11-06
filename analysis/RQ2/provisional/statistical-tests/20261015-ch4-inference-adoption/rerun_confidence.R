#!/usr/bin/env Rscript
# Refit every member of the existing confidence Holm-15 family in a fresh folder.
library(ordinal)
options(contrasts=c('contr.treatment','contr.poly'))
args<-commandArgs(trailingOnly=TRUE)
base<-normalizePath(args[1])
out<-file.path(base,'analysis/RQ2/provisional/statistical-tests/20261015-ch4-inference-adoption')
d<-read.csv(file.path(out,'input.csv'))
stopifnot(nrow(d)==72,length(unique(d$participant_id))==24,all(d$Q1_confidence%in%1:4),all(d$Q2_confidence%in%1:4))
d$gap<-d$Q1_confidence-d$Q2_confidence
scopes<-list(all=d,animated=d[d$condition!='NT',],NT=d[d$condition=='NT',])
rows<-list()
add_t<-function(v,id,first=NA_real_,second=NA_real_,primary=FALSE){
  q<-t.test(v,mu=0)
  rows[[length(rows)+1]]<<-data.frame(test_id=id,method='paired_t',n_pairs=length(v),first_mean=first,second_mean=second,gap=mean(v),raw_p=q$p.value,ci95_low=q$conf.int[1],ci95_high=q$conf.int[2],primary=primary)
}
for(nm in names(scopes)){
 a<-aggregate(cbind(Q1_confidence,Q2_confidence)~participant_id,scopes[[nm]],mean)
 add_t(a$Q1_confidence-a$Q2_confidence,paste0('prior_t_',nm),mean(a$Q1_confidence),mean(a$Q2_confidence),TRUE)
}
for(p in list(c('V1','V2'),c('V1','V3'),c('V2','V3'))){
 a<-d[d$condition==p[1],c('participant_id','gap')];b<-d[d$condition==p[2],c('participant_id','gap')]
 z<-merge(a,b,by='participant_id');stopifnot(nrow(z)==8)
 add_t(z$gap.x-z$gap.y,paste0('prior_t_',paste(p,collapse='-')))
}
long<-rbind(transform(d,question='Q1',rating=Q1_confidence),transform(d,question='Q2',rating=Q2_confidence))
long$rating<-ordered(long$rating,levels=1:4)
long$question<-factor(long$question,levels=c('Q2','Q1'))
long$condition<-factor(long$condition,levels=c('NT','V1','V2','V3'))
long$position<-factor(long$trial_number)
long$participant_id<-factor(long$participant_id)
long$trial_id<-factor(long$participant_trial_key)
fixed<-~question*condition+question*position
X<-model.matrix(fixed,long);stopifnot(qr(X)$rank==ncol(X))
m<-clmm(rating~question*condition+question*position+(1|participant_id)+(1|trial_id),data=long,
 link='logit',threshold='flexible',Hess=TRUE,nAGQ=1,
 control=clmm.control(method='nlminb',maxIter=1000,gradTol=1e-7,rel.tol=1e-10,iter.max=1000))
diag<-list(convergence=m$optRes$convergence,max_gradient=max(abs(m$gradient)),min_hessian_eigenvalue=min(eigen(m$Hessian,symmetric=TRUE,only.values=TRUE)$values),hessian_condition=kappa(m$Hessian))
stopifnot(diag$convergence==0,diag$max_gradient<.001,diag$min_hessian_eigenvalue>0,diag$hessian_condition<1e8)
capture.output(diag,file=file.path(out,'ordinal_fit_diagnostics.txt'))
saveRDS(m,file.path(out,'ordinal_fit.rds'))
ordinal_rows<-list()
add_o<-function(z,id){
 z1<-z;z1$question<-factor('Q1',levels=levels(long$question))
 z2<-z;z2$question<-factor('Q2',levels=levels(long$question))
 v<-colMeans(model.matrix(fixed,z1)-model.matrix(fixed,z2))[names(m$beta)]
 est<-sum(v*m$beta);se<-sqrt(drop(t(v)%*%vcov(m)[names(v),names(v)]%*%v))
 ordinal_rows[[length(ordinal_rows)+1]]<<-data.frame(test_id=id,log_odds_shift=est,se=se,raw_p=2*pnorm(-abs(est/se)))
 rows[[length(rows)+1]]<<-data.frame(test_id=id,method='ordinal_model_wald',n_pairs=length(unique(z$participant_id)),first_mean=NA_real_,second_mean=NA_real_,gap=NA_real_,raw_p=2*pnorm(-abs(est/se)),ci95_low=NA_real_,ci95_high=NA_real_,primary=FALSE)
}
for(nm in names(scopes)){
 z<-long[long$question=='Q2'&(nm=='all'|(nm=='animated'&long$condition!='NT')|(nm=='NT'&long$condition=='NT')),]
 add_o(z,paste0('prior_ordinal_',nm))
}
for(cn in c('V1','V2','V3')){
 z<-d[d$condition==cn,]
 add_t(z$gap,paste0('within_t_',cn),mean(z$Q1_confidence),mean(z$Q2_confidence),TRUE)
}
for(cn in c('V1','V2','V3')) add_o(long[long$question=='Q2'&long$condition==cn,],paste0('within_ordinal_',cn))
family<-do.call(rbind,rows);stopifnot(nrow(family)==15)
family$holm_p<-p.adjust(family$raw_p,'holm')
family$supported<-family$holm_p<.05
write.csv(family,file.path(out,'confidence_family15.csv'),row.names=FALSE)
write.csv(family[family$primary,],file.path(out,'mean_confidence_tests.csv'),row.names=FALSE)
write.csv(do.call(rbind,ordinal_rows),file.path(out,'ordinal_contrasts.csv'),row.names=FALSE)
capture.output(sessionInfo(),file=file.path(out,'R_session_info.txt'))
cat('15 confidence tests recomputed; ordinal fit diagnostics passed\n')
