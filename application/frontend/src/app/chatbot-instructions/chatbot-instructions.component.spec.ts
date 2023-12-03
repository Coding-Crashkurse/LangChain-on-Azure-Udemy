import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ChatbotInstructionsComponent } from './chatbot-instructions.component';

describe('ChatbotInstructionsComponent', () => {
  let component: ChatbotInstructionsComponent;
  let fixture: ComponentFixture<ChatbotInstructionsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ChatbotInstructionsComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ChatbotInstructionsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
