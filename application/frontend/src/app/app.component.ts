import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Food } from './food-card/food.models';
import { FoodCardComponent } from './food-card/food-card.component';
import { ChatbotInstructionsComponent } from './chatbot-instructions/chatbot-instructions.component';
import { ChatUiComponent } from './chat-ui/chat-ui.component';
import { HeaderComponent } from './header/header.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [
    CommonModule,
    FoodCardComponent,
    ChatbotInstructionsComponent,
    ChatUiComponent,
    HeaderComponent,
  ],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css',
})
export class AppComponent {
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
