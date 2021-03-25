import { Component, OnInit } from '@angular/core';
import { MoviesService, Movie } from '../../services/movies.service';
import { ModalController } from '@ionic/angular';
import { MovieFormComponent } from './movie-form/movie-form.component';
import { AuthService } from 'src/app/services/auth.service';

@Component({
  selector: 'app-movies',
  templateUrl: './movies.page.html',
  styleUrls: ['./movies.page.scss'],
})
export class MovieMenuPage implements OnInit {
  Object = Object;

  constructor(
    private auth: AuthService,
    private modalCtrl: ModalController,
    public movies: MoviesService
    ) { }

  ngOnInit() {
    this.movies.getMovies();
  }

  async openForm(activemovie: Movie = null) {
    if (!this.auth.can('patch:movies')  && !this.auth.can('post:movies')) {
      return;
    }

    const modal = await this.modalCtrl.create({
      component: MovieFormComponent,
      componentProps: { movie: activemovie, isNew: !activemovie }
    });

    modal.present();
  }

}
