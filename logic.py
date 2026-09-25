''' This is where simple logic functions are defined.'''

def main():
    '''This is used to to show how much work is going to be done based on how many people are 
    located in the file'''
    def size_score():
        pass

    ''' Measures how complex the data is to be processed.(more data changes, calulations, or dependents will increase the score)
    Based on:
    Demo processsing complexity
    Need to calculate ACA Status
    Client has ACA status changes
    ACA status processsing complexity
    Client had BG status changes
    BG status processing complexity
    Need to prcess transfers 
    Employment processsing complexity
    Enrollemt processsing complexity
    COBRA processsing complexity
    Dependents processsing complexity
    Data quality'''
    def processing_score():
        pass

    ''' Measures how many manual effort was required. (more changes will increase the score)
    (Amount of manual changes ÷ 5), rounded up to the next whole number.'''
    def manual_change_score():
        pass

    ''' Measures how many conflicts were found in the data. (more conflicts will increase the score)
    (Amount of conflicts ÷ 30), rounded up to the next whole number.'''
    def conflict_score():
        pass
    
    ''' Measures additional effort for clients loaded through the monthly loader.
    (Number of people × 0.001)'''
    def monthly_loaded_score():
        pass
    
    '''This function calculates the total score based on the individual scores from size, processing, manual changes, conflicts, and monthly loaded data.'''
    def total_score():
        score = 0        
        score += size_score()
        score += processing_score()
        score += manual_change_score()
        score += conflict_score()
        score += monthly_loaded_score()

        return score


if __name__ == "__main__":
    main()

