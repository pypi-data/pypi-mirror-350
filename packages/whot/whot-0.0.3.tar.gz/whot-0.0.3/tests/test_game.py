import unittest
from whot import *

class TestSpecialCards(unittest.TestCase):
    
    def test_pick_two(self):
        pile = Card(Suit.CIRCLE, 3)

        card1 = Card(Suit.CIRCLE, 2)
        card2 = Card(Suit.WHOT, 20)

        card3 = Card(Suit.TRIANGLE, 1)
        card4 = Card(Suit.WHOT, 20)

        card5 = Card(Suit.STAR, 1)
        card6 = Card(Suit.STAR, 2) 

        card7 = Card(Suit.STAR, 3)
        card8 = Card(Suit.STAR, 4)


        test_players = [[card1, card2], [card3, card4], [card5, card6], [card7, card8]]

        w = TestWhot(pile, test_players)

        w.start_game()

        w.play(0)

        self.assertEqual(len(w.game_state()["player_1"]), 1)
        self.assertEqual(len(w.game_state()["player_2"]), 4)
        self.assertEqual(len(w.game_state()["player_3"]), 2)
        self.assertEqual(len(w.game_state()["player_3"]), 2)

        self.assertEqual(w.game_state()["current_player"], "player_3")

    def test_go_gen(self):
        pile = Card(Suit.CIRCLE, 3)

        card1 = Card(Suit.CIRCLE, 14)
        card2 = Card(Suit.WHOT, 20)

        card3 = Card(Suit.TRIANGLE, 1)
        card4 = Card(Suit.WHOT, 20)

        card5 = Card(Suit.STAR, 1)
        card6 = Card(Suit.STAR, 2) 

        card7 = Card(Suit.STAR, 3)
        card8 = Card(Suit.STAR, 4)

        test_players = [[card1, card2], [card3, card4], [card5, card6], [card7, card8]]

        w = TestWhot(pile, test_players)

        w.start_game()

        w.play(0)

        self.assertEqual(len(w.game_state()["player_1"]), 1)
        self.assertEqual(len(w.game_state()["player_2"]), 3)
        self.assertEqual(len(w.game_state()["player_3"]), 3)
        self.assertEqual(len(w.game_state()["player_3"]), 3)

    def test_suspension(self):
        pile = Card(Suit.CIRCLE, 3)

        card1 = Card(Suit.CIRCLE, 8)
        card2 = Card(Suit.WHOT, 20)

        card3 = Card(Suit.TRIANGLE, 1)
        card4 = Card(Suit.WHOT, 20)

        card5 = Card(Suit.STAR, 1)
        card6 = Card(Suit.STAR, 2) 


        test_players = [[card1, card2], [card3, card4], [card5, card6]]

        w = TestWhot(pile, test_players)

        w.start_game()

        w.play(0)

        self.assertEqual(w.game_state()["current_player"], "player_3")    

    def test_hold_on(self):
        pile = Card(Suit.CIRCLE, 3)

        card1 = Card(Suit.CIRCLE, 1)
        card2 = Card(Suit.CIRCLE, 4)
        card3 = Card(Suit.WHOT, 20)

        card4 = Card(Suit.TRIANGLE, 5)
        card5 = Card(Suit.STAR, 7)
        card6 = Card(Suit.SQUARE, 10)

        test_players = [[card1, card2, card3], [card4, card5, card6]]

        w = TestWhot(pile, test_players)

        w.start_game()

        w.play(0)

        self.assertEqual(w.game_state()["current_player"], "player_1")    

        w.play(0)

        self.assertEqual(len(w.game_state()["player_1"]), 1)
        self.assertEqual(w.game_state()["current_player"], "player_2")


    def test_whot(self):
        pile = Card(Suit.SQUARE, 3)

        card1 = Card(Suit.CIRCLE, 1)
        card2 = Card(Suit.CIRCLE, 4)
        card3 = Card(Suit.WHOT, 20)

        card4 = Card(Suit.SQUARE, 5)
        card5 = Card(Suit.CIRCLE, 10)
        card6 = Card(Suit.SQUARE, 11)

        card7 = Card(Suit.STAR, 8)
        card8 = Card(Suit.STAR, 2)
        card9 = Card(Suit.CROSS, 11)

        test_players = [[card1, card2, card3], [card4, card5, card6], [card7, card8, card9]]
        
        w = TestWhot(pile, test_players)

        w.start_game()

        w.play(2)
        self.assertEqual(w.game_state()["current_player"], "player_1")    

        w.request("circle")
        
        self.assertEqual(w.request_mode, True)

        self.assertEqual(w.game_state()["current_player"], "player_2")

        w.market()

        self.assertEqual(w.game_state()["current_player"], "player_3")


class TestIntialCards(unittest.TestCase):
    """
    These test cases are used to test when there's a 
    special card as the initial card on the pile.
    """

    def test_pick_two(self):
        """
        This test case is used to test when the inital card 
        on the deck is 2.
        """
        
        pile = Card(Suit.CIRCLE, 2)

        card1 = Card(Suit.CIRCLE, 3)
        card2 = Card(Suit.WHOT, 20)

        card3 = Card(Suit.TRIANGLE, 1)
        card4 = Card(Suit.WHOT, 20)

        card5 = Card(Suit.STAR, 1)
        card6 = Card(Suit.STAR, 2) 

        card7 = Card(Suit.STAR, 3)
        card8 = Card(Suit.STAR, 4)


        test_players = [[card1, card2], [card3, card4], [card5, card6], [card7, card8]]

        w = TestWhot(pile, test_players)

        w.start_game()

        self.assertEqual(len(w.game_state()["player_1"]), 4)
        self.assertEqual(len(w.game_state()["player_2"]), 2)
        self.assertEqual(len(w.game_state()["player_3"]), 2)
        self.assertEqual(len(w.game_state()["player_3"]), 2)        
    
    def test_go_gen(self):
        """
        This test case is used to test when the inital card 
        on the deck is 14.
        """

        pile = Card(Suit.CIRCLE, 14)

        card1 = Card(Suit.CIRCLE, 3)
        card2 = Card(Suit.WHOT, 20)

        card3 = Card(Suit.TRIANGLE, 1)
        card4 = Card(Suit.WHOT, 20)

        card5 = Card(Suit.STAR, 1)
        card6 = Card(Suit.STAR, 2) 

        card7 = Card(Suit.STAR, 3)
        card8 = Card(Suit.STAR, 4)

        test_players = [[card1, card2], [card3, card4], [card5, card6], [card7, card8]]

        w = TestWhot(pile, test_players)

        w.start_game()

        self.assertEqual(len(w.game_state()["player_1"]), 3)
        self.assertEqual(len(w.game_state()["player_2"]), 3)
        self.assertEqual(len(w.game_state()["player_3"]), 3)
        self.assertEqual(len(w.game_state()["player_3"]), 3)


    def test_suspension(self):
        """
        This test case is used to test when the inital card 
        on the deck is 8.
        """

        pile = Card(Suit.CIRCLE, 8)

        card1 = Card(Suit.CIRCLE, 3)
        card2 = Card(Suit.WHOT, 20)

        card3 = Card(Suit.TRIANGLE, 1)
        card4 = Card(Suit.WHOT, 20)

        card5 = Card(Suit.STAR, 1)
        card6 = Card(Suit.STAR, 2) 


        test_players = [[card1, card2], [card3, card4], [card5, card6]]

        w = TestWhot(pile, test_players)

        w.start_game()

        self.assertEqual(w.game_state()["current_player"], "player_2")
    
    def test_whot(self):
        """
        This test case is used to test when the inital card 
        on the deck is whot.
        """
                
        pile = Card(Suit.WHOT, 20)

        card1 = Card(Suit.CIRCLE, 1)
        card2 = Card(Suit.CIRCLE, 4)
        card3 = Card(Suit.SQUARE, 3)

        card4 = Card(Suit.SQUARE, 5)
        card5 = Card(Suit.CIRCLE, 10)
        card6 = Card(Suit.SQUARE, 11)

        card7 = Card(Suit.STAR, 8)
        card8 = Card(Suit.STAR, 2)
        card9 = Card(Suit.CROSS, 11)

        test_player = [[card1, card2, card3], [card4, card5, card6], [card7, card8, card9]]
        
        w = TestWhot(pile, test_player)

        w.start_game()

        result = w.play(0)
        self.assertEqual(result["status"], "Failed")    


        self.assertEqual(w.game_state()["current_player"], "player_1")


if __name__ == '__main__':
    unittest.main()