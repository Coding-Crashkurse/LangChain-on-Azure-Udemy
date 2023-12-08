import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  private isAuthenticated: boolean = false;

  constructor() {}

  login(username: string, password: string): boolean {
    this.isAuthenticated = username === 'admin' && password === 'admin';
    return this.isAuthenticated;
  }

  checkAuthentication(): boolean {
    return this.isAuthenticated;
  }
}
