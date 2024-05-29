from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle  0
# A says "I am both a knight and a knave."
knowledge0 = And(
    # TODO
    #************************************************************************
    # (1) information given in the definition of a Knight and Knave puzzle
    #************************************************************************
    # a Character cannot be both a knight and a knave at the same time
        Not(And(AKnight, AKnave)),
    # a Character s either a knight or a knave
        Or(AKnight, AKnave),

    #************************************************************************
    # (2) information about what the characters actually said
    #************************************************************************
    # If A Character is a knight, then the statement 
    # "I am both a knight and a knave" must be true because Knight always tell the true
        Implication(AKnight, And(AKnight, AKnave)),
    # If A Character is a knave, then the statement 
    #"I am both a knight and a knave" must be false  because Knave always lie
        Implication(AKnave, Not(And(AKnight, AKnave)))
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    # TODO
    #************************************************************************
    # (1) information given in the definition of a Knight and Knave puzzle
    #************************************************************************
    # a Character cannot be both a knight and a knave at the same time
        Not(And(AKnight, AKnave)),
        Not(And(BKnight, BKnave)),
    # a Character s either a knight or a knave
        Or(AKnight, AKnave),
        Or(BKnight, BKnave),

    #************************************************************************
    # (2) information about what the characters actually said
    #************************************************************************
    # A's statement: "We are both knaves."
    # If A is a knight, then both A and B are knaves, because Knight always tell the true
        Implication(AKnight, And(AKnave, BKnave)),
    # If A is a knave, then it's not true that both A and B are knaves, because Knave always lie
        Implication(AKnave, Not(And(AKnave, BKnave)))

    #************************************************************************

)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    # TODO
    #************************************************************************
    # (1) information given in the definition of a Knight and Knave puzzle
    #************************************************************************
    # a Character cannot be both a knight and a knave at the same time
        Not(And(AKnight, AKnave)),
        Not(And(BKnight, BKnave)),
    # a Character s either a knight or a knave
        Or(AKnight, AKnave),
        Or(BKnight, BKnave),

    #************************************************************************
    # (2) information about what the characters actually said
    #************************************************************************
    # 'A' say "We are the same kind."
    Implication(AKnight, Or(And(AKnight, BKnight), And(AKnave, BKnave))),
    Implication(AKnave, Not(Or(And(AKnight, BKnight), And(AKnave, BKnave)))),
    # 'B' say "We are of different kinds."
    Implication(BKnight, Or(And(AKnight, BKnave), And(AKnave, BKnight))),
    Implication(BKnave, Not(Or(And(AKnight, BKnave), And(AKnave, BKnight))))
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    # TODO
    #************************************************************************
    # (1) information given in the definition of a Knight and Knave puzzle
    #************************************************************************
    # a Character cannot be both a knight and a knave at the same time
        Not(And(AKnight, AKnave)),
        Not(And(BKnight, BKnave)),
        Not(And(CKnight, CKnave)),
    # a Character s either a knight or a knave
        Or(AKnight, AKnave),
        Or(BKnight, BKnave),
        Or(CKnight, CKnave),

    #************************************************************************
    # (2) information about what the characters actually said
    #************************************************************************
    # 1
    # A says either "I am a knight." or "I am a knave.", but you don't know which.        
    # If A is a knight, It is true that 'A' can be a  knight" or "knave".
    # We don't know which, so we consider both possibilities.
        Implication(AKnight, Or(AKnight, AKnave)),
        Implication(AKnave, Not(Or(AKnight, AKnave))),

    # 2
    # B says "A said 'I am a knave'."
    # If B is a knight, then A said "I am a knave" is true
        Implication(BKnight, AKnave),
    # If B is a knave, then B's statement about A is false (A did not say "I am a knave")
        Implication(BKnave, Not(AKnave)),

    # 3
    # B says "C is a knave."
    # If B is a knight, then "C said 'I am a knave'" is true
        Implication(BKnight, CKnave),
    # If B is a knave, then "C said 'I am a knave'" is false
        Implication(BKnave, Not(CKnave)),

    # 4
    # C says "A is a knight."
    # If C is a knight, then "C said 'A is a knight.' " is true
        Implication(CKnight, AKnight),
    # If C is a knave, then "C said 'A is a knight.' " is false        
        Implication(CKnave, Not(AKnight))
)



def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
