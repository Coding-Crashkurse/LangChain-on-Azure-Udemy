import { ComponentFixture, TestBed } from '@angular/core/testing';

import { FoodCardComponent } from './food-card.component';

describe('FoodCardComponent', () => {
  let component: FoodCardComponent;
  let fixture: ComponentFixture<FoodCardComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ FoodCardComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(FoodCardComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
