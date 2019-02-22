package main

import(
	"fmt"
)



func main() {
	Counting_of_players()

}


//Player sign up
type Player_data struct {
	name string
	age int
}

func Counting_of_players() {
	fmt.Print("How many players:")
	var count_of_players int
	fmt.Scan(&count_of_players)

	if count_of_players > 1{
		for i := 1;i <= count_of_players; {
			for j := 1;j <= len(count_of_players);j++{
				var count [j]int
			}
			Player_autorization(count)
			i++
		}
	}else if count_of_players == 0 {
		fmt.Println("not correct")
		}else {Player_autorization()}
}

func Player_autorization(id) {
	player := Player_data{}

	for i := 1; i <= ;i++{
		for i := 0; i < count; i++ {
			fmt.Print("what's your name:")
			fmt.Scan(&player.name)

			fmt.Print("How old are you:")
			fmt.Scan(&player.age)
		}
	}
}
