import { Component } from '@angular/core';
import { Food } from './food-card/food.models'; // Ensure this path is correct

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
})
export class AppComponent {
  title = 'frontend';

  // Correctly declare the foods array
  foods: Food[] = [
    {
      imageUrl: '/assets/pizza-margherita.png',
      name: 'Pizza Margherita',
      price: 10.99,
    },
    {
      imageUrl: '/assets/pizza-salami.png',
      name: 'Pizza Salami',
      price: 11.99,
    },
    {
      imageUrl: '/assets/pizza-quattro-formaggi.png',
      name: 'Pizza Quattro Formaggi',
      price: 13.99,
    },
    {
      imageUrl: '/assets/marshmallow-pizza.png',
      name: 'Marshmallow Pizza',
      price: 14.99,
    },
  ];
}
