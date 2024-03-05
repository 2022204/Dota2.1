console.log("Hello World!")

//Comments 
/*
Comments just like c++
*/

/*
Operators are
+,-,/,*,%, ** (power)
    5**2 = 5^2

a++,b++, increment decrement;
a+=2 . a= a+2;

comparision
== equal to. === equalto and type
!= not equal to, !== not equal to and type too

5 == "5" -> true
5 === "5" -> false
*/

let a  = 5;
let b = 3;
let c = "5"
console.log(a+b);
console.log(a==c, a===c);

/*
Logical Operators
AND &&
OR ||
NOT !
*/
/*
Conditional Statement


*/
// let color;
// if(mode === "dark-mode"){
//     color = "black";
// }
// else{ ....
//}

if(a < 18){
    console.log(a);
}

let result = b >= 3  ? "B>=3":"B<3";  //Compact if-else
console.log(result);

const expr = "Papayas";
switch(expr){
    case 'Oranges':
        console.log('Oranges');
        break;
    case 'Papayas':
        console.log('Papayas');
        break;
    default:
        console.log("Can't know");
        break;
    }

let name = prompt("Name: ");
console.log(name);