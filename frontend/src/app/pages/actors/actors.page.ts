import { Component, OnInit } from '@angular/core';
import { ActorsService, Actor } from '../../services/actors.service';
import { ModalController } from '@ionic/angular';
import { ActorFormComponent } from './actor-form/actor-form.component';
import { AuthService } from 'src/app/services/auth.service';

@Component({
  selector: 'app-actors',
  templateUrl: './actors.page.html',
  styleUrls: ['./actors.page.scss'],
})
export class ActorMenuPage implements OnInit {
  Object = Object;

  constructor(
    private auth: AuthService,
    private modalCtrl: ModalController,
    public actors: ActorsService
    ) { 
      console.log("in actors page : ", actors);
    }

  ngOnInit() {
    this.actors.getActors();
  }

  async openForm(activeactor: Actor = null) {
    if (!this.auth.can('patch:actors') && !this.auth.can('post:actors')) {
      return;
    }

    const modal = await this.modalCtrl.create({
      component: ActorFormComponent,
      componentProps: { actor: activeactor, isNew: !activeactor }
    });

    modal.present();
  }

}
