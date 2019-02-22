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

	var id_c int = count_of_players

	if count_of_players > 1{
		for i := 1;i <= count_of_players; {
			Player_autorization(id_c)
			i++
		}
	}else if count_of_players == 0 {
		fmt.Println("not correct")
		}else {
			id_c = 1
			Player_autorization(id_c)}
}

func Player_autorization(id_p int) {
	player := Player_data{}

	for i := 1;i <= id_p;{
		fmt.Print("what's your name:")
		fmt.Scan(&player.name)

		fmt.Print("How old are you:")
		fmt.Scan(&player.age)
		i++
		fmt.Print(id_p," ", player.name," ", player.age)
	}
}
