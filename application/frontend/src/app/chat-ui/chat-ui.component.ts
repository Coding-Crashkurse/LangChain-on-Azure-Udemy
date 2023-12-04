import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';

interface ChatMessage {
  text: string;
  sender: 'bot' | 'user';
}

@Component({
  selector: 'app-chat-ui',
  templateUrl: './chat-ui.component.html',
  styleUrls: ['./chat-ui.component.css'],
})
export class ChatUiComponent implements OnInit {
  public isVisible: boolean = false;
  public messages: ChatMessage[] = [];
  public newMessage: string = '';

  constructor(private http: HttpClient) {}

  ngOnInit(): void {}

  toggleChat(): void {
    this.messages = [];
    this.newMessage = '';
    this.isVisible = !this.isVisible;
  }

  sendUserMessage(): void {
    if (this.newMessage.trim()) {
      this.messages.push({ text: this.newMessage, sender: 'user' });
      this.sendMessageToApi(this.newMessage, this.messages);
      this.newMessage = '';
    }
  }

  sendMessageToApi(newMessage: string, conversation: ChatMessage[]): void {
    const backendHost = process.env['BACKEND_HOST'] || 'localhost';
    const apiUrl = `http://${backendHost}:8000/conversation`;
    this.http
      .post<any>(apiUrl, {
        question: newMessage,
        conversation: conversation.map((msg) => ({
          role: msg.sender,
          content: msg.text,
        })),
      })
      .subscribe((response) => {
        this.messages.push({ text: response.response, sender: 'bot' });
      });
  }
}
