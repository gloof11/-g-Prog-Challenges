const readline = require("readline-sync");

let userInput = readline.question("Enter a sentence: ");
let RotValue = 13;
FinalOut = "";

userInput.split('').forEach((letter) => {

    FinalOut.concat(letter)
})

console.log(FinalOut)