import pandas as pd
from datetime import date
import argparse

def name_return(amount=1,real=True, pop_weighted=None, gender=None, age_min=None, age_max=None):
    if real:
        names=pd.read_csv('./namegen_data/name_data.csv', index_col=0)
        
        #if asked for gender neutral names, restrict ourselves with names with a high nbscore
        if gender=='n':
            names=names[names['nb_score']>2/3] 
        
        if gender=='f':
            names=names[names['gender']=='F']
            
        if gender=='m':
            names=names[names['gender']=='M']
        
        #since the data is in terms of birth years rather than ages, 
        #we need to know what year it is when given age filters
        #if given an age minimum, we figure out the last year someone can be born to be that age or older
        #and the other way around for age maximums
        current_year=date.today().year 
        
        if age_min!=None:
            max_year=current_year-age_min
            names=names[names['year']<=max_year]
        
        if age_max!=None:
            min_year=current_year-age_max
            names=names[names['year']>=min_year]
            
        if pop_weighted=='regular':
            weights=names['count']
        elif pop_weighted=='inverse':
            weights=names['rarity']
        else:
            weights=None
        
        output=names['name'].sample(n=amount, weights=weights).to_numpy()
        
        
    else:
        names=pd.read_csv('./namegen_data/generated_names.txt', sep='\n', names=['name'])
        output=names['name'].sample(n=amount).to_numpy()
        
    for name in output:
        print(name)
        
parser = argparse.ArgumentParser()
parser.add_argument("-n","--number", default=1, type=int, help="number of names to output")
parser.add_argument("-f", "--fake", help="output generated names rather than existing ones", action="store_false")
parser.add_argument("-p", "--popularity", type=int, help="1 is popularity weighting, -1 is inverse weighting, 0 is no weighting", choices=[-1,0,1], default=0)
parser.add_argument("-g", "--gender", type=str, help="m returns masculine names, f returns feminine names, n returns gender-neutral names", choices=["m","f","n"])
parser.add_argument("--agemin", type=int, help="will return names older than this age")
parser.add_argument("--agemax", type=int, help="will return names younger than this age")

args=parser.parse_args()

if args.popularity==1:
    weights="regular"
elif args.popularity==-1:
    weights="inverse"
else:
    weights=None

name_return(amount=args.number, real=args.fake, pop_weighted=weights, gender=args.gender, age_min=args.agemin, age_max=args.agemax)