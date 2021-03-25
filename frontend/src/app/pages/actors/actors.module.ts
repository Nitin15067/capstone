import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Routes, RouterModule } from '@angular/router';

import { IonicModule } from '@ionic/angular';

import { ActorMenuPage } from './actors.page';
import { ActorFormComponent } from './actor-form/actor-form.component';

const routes: Routes = [
  {
    path: '',
    component: ActorMenuPage
  }
];

@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    IonicModule,
    RouterModule.forChild(routes)
  ],
  entryComponents: [ActorFormComponent],
  declarations: [ActorMenuPage, ActorFormComponent],
})
export class ActorsPageModule {}
