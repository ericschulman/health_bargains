

`param_list = [[25,5,.5,.5,0,0],[20,5,.5,.5,0,0],[25,10,.5,.5,0,0],[25,5,.5,.1,0,0],[25,5,.1,.5,0,0],[25,5,.5,.5,3,3]]`

for i in range(len(param_list)):
    seq_result,active_result,passive_result = gen_data(param_list[i],nobs=10000,var=5)
    seq_result.to_csv('fake_data/seq_data_%s.csv'%i)
    active_result.to_csv('fake_data/active_data_%s.csv'%i)
    passive_result.to_csv('fake_data/passive_data_%s.csv'%i)


- Note the test will very likely reject when beta1=beta2... there arent' enough moment conditions... singular covaraince matrix...
- betas in the model don't actually seem to be indetified...
- p1 and p2 are the same on average according to the model... as a result... really on 3 moment conditions...
- what if i just do beta1 and beta2? and ignore v, l and mc?

=====
- issue with my test is non-linearities break the test...
- issue with davids test power... i just aggregated the dataframes incorrectly...