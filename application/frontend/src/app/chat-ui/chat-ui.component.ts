import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-chat-ui',
  templateUrl: './chat-ui.component.html',
  styleUrls: ['./chat-ui.component.css'],
})
export class ChatUiComponent implements OnInit {
  public isVisible: boolean = false;
  public messages: { text: string; sender: 'bot' | 'user' }[] = [];
  public newMessage: string = ''; // Add this line

  constructor() {}

  ngOnInit(): void {
    // You can initialize your messages here if needed
  }

  toggleChat(): void {
    this.isVisible = !this.isVisible;
  }

  sendUserMessage(): void {
    if (this.newMessage.trim()) {
      this.messages.push({ text: this.newMessage, sender: 'user' });
      // Simulate a bot response
      setTimeout(() => {
        this.messages.push({
          text: 'This is an automated response from the bot.',
          sender: 'bot',
        });
      }, 1000);
      this.newMessage = '';
    }
  }
}
