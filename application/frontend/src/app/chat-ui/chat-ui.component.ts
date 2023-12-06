import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../environments/environment';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';

interface ChatMessage {
  text: string;
  sender: 'bot' | 'user';
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
      this.messages.push({ text: this.newMessage, sender: 'user' });
      this.sendMessageToApi(this.newMessage, this.messages);
      this.newMessage = '';
    }
  }

  sendMessageToApi(newMessage: string, conversation: ChatMessage[]): void {
    const apiUrl = `${
      environment.backendHost
    }/conversation?question=${encodeURIComponent(newMessage)}`;
    const payload = {
      conversation: conversation.map((msg) => ({
        role: msg.sender,
        content: msg.text,
      })),
    };

    console.log('Sending to API:', payload);

    this.http.post<any>(apiUrl, payload).subscribe((response) => {
      this.messages.push({ text: response.answer, sender: 'bot' });
    });
  }
}
