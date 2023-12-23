import { Component, OnInit } from '@angular/core';
import { environment } from '../../environments/environment';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { HttpClient, HttpParams } from '@angular/common/http';

interface ChatMessage {
  text: string;
  sender: 'bot' | 'user';
  isLoading?: boolean; // Optional property for loading state
}

@Component({
  selector: 'app-chat-ui',
  templateUrl: './chat-ui.component.html',
  styleUrls: ['./chat-ui.component.css'],
  standalone: true,
  imports: [FormsModule, CommonModule],
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
      // Add user's message to the chat
      this.messages.push({ text: this.newMessage, sender: 'user' });

      // Add a loading indicator for bot's response
      this.messages.push({ text: '', sender: 'bot', isLoading: true });

      // Send message to API
      this.sendMessageToApi(this.newMessage);
      this.newMessage = '';
    }
  }

  sendMessageToApi(newMessage: string): void {
    const apiUrl = `${environment.backendHost}/conversation`;
    const params = new HttpParams().set('question', newMessage);
    const payload = {
      conversation: this.messages.map((msg) => ({
        role: msg.sender,
        content: msg.text,
      })),
    };

    this.http.post<any>(apiUrl, payload, { params }).subscribe((response) => {
      this.messages.pop(); // Remove the loading indicator
      this.messages.push({ text: response.answer, sender: 'bot' });
    });
  }
}
