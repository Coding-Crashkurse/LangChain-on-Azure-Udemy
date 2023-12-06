import { Component, Input } from '@angular/core';
import { Food } from './food.models';

@Component({
  selector: 'app-food-card',
  templateUrl: './food-card.component.html',
  styleUrls: ['./food-card.component.css'],
  standalone: true,
})
export class FoodCardComponent {
  @Input() food!: Food;
}
