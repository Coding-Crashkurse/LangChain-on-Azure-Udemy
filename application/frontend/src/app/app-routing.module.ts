import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { RootcompComponent } from './rootcomp/rootcomp.component';
import { AdminComponent } from './admin/admin.component';

const routes: Routes = [
  { path: '', component: RootcompComponent },
  { path: 'admin', component: AdminComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
})
export class AppRoutingModule {}
