import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { ChatUiComponent } from './chat-ui/chat-ui.component';
import { FoodCardComponent } from './food-card/food-card.component';
import { HeaderComponent } from './header/header.component';
import { ChatbotInstructionsComponent } from './chatbot-instructions/chatbot-instructions.component';

@NgModule({
  declarations: [
    AppComponent,
    ChatUiComponent,
    FoodCardComponent,
    HeaderComponent,
    ChatbotInstructionsComponent,
  ],
  imports: [
    HttpClientModule,
    BrowserModule,
    AppRoutingModule,
    FormsModule,
    CommonModule,
  ],
  providers: [],
  bootstrap: [AppComponent],
})
export class AppModule {}
