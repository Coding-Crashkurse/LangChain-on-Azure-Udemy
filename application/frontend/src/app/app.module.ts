import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule } from '@angular/forms'; // Add this line

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
    BrowserModule,
    AppRoutingModule,
    FormsModule, // Add this here
  ],
  providers: [],
  bootstrap: [AppComponent],
})
export class AppModule {}
