

def f(p):
    # if p>2*p_star:
    #     print('ZBYT DUUUZE p !',p)
    # if p<0:
    #     print('ZBYT MALE p !')
    return p*lambda_ if p<p_star else lambda_*(2*p_star-p)
def p_start(previous_densities):
    return 0.25 *(lb+2*previous_densities[0]+previous_densities[1])-0.5*(f(previous_densities[1])-f(lb))
def p_center(previous_densities,k):
    return 0.25*(previous_densities[k-1]+2*previous_densities[k]+previous_densities[k+1])-0.5*(f(previous_densities[k+1])-f(previous_densities[k-1]))
def p_last(previous_densities):
    n=len(previous_densities)-1
    # gamma_out=p_last(previous_densities)
    return 0.25*(previous_densities[n-1]+2*previous_densities[n]+rb)-0.5*(f(rb)-f(previous_densities[n-1]))
def p_new_count(previous_densities):
    new_densities = []
    for i in range(len(previous_densities)):
        if i == 0:
            new_densities.append(p_start(previous_densities))
        elif i == len(previous_densities)-1:
            new_densities.append(p_last(previous_densities))
        else:
            new_densities.append(p_center(previous_densities,i))
    return new_densities


lambda_=1
p_star=6
n=8
lb=0
rb=12
# gamma_in=0
# gamma_out=0
densities = [2,5,4,3,6,2,1,4,2]
# print(p_start(densities))
# print(p_center(densities,2))
for i in range(4):
    densities = p_new_count(densities)
    print(densities)
    # print(sum(densities))