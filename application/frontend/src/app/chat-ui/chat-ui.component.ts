import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-chat-ui',
  templateUrl: './chat-ui.component.html',
  styleUrls: ['./chat-ui.component.css'],
})
export class ChatUiComponent implements OnInit {
  // You can declare properties and methods here
  // For example, a flag to toggle chat visibility
  public isVisible: boolean = false;

  constructor() {}

  ngOnInit(): void {
    // Initialization logic can go here
  }

  // Method to toggle the chat UI
  toggleChat(): void {
    this.isVisible = !this.isVisible;
  }
}
