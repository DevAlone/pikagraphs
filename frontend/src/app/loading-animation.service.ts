import { Injectable, Output, EventEmitter } from '@angular/core';

@Injectable()
export class LoadingAnimationService {
  @Output()
  runningChanged = new EventEmitter<boolean>();

  private IMAGES_COUNT = 19;
  images: string[] = [];

  currentImage = '';
  counter = 0;

  constructor() {
    for (let i = 0; i < this.IMAGES_COUNT; ++i) {
      this.images.push((i + 1) + '.gif');
    }

    this.changeImage();
  }

  get isRunning(): boolean {
    return this.counter > 0;
  }

  public start(): void {
    if (this.counter === 0) {
      this.runningChanged.emit(true);
    }

    ++this.counter;
  }

  public stop(): void {
    if (this.counter === 1) {
      this.runningChanged.emit(false);
      // this.changeImage();
    }

    --this.counter;
    if (this.counter < 0) {
      this.counter = 0;
    }
  }

  public getImagePath(): string {
    return this.currentImage;
  }

  public changeImage(): void {
    const image = this.images[Math.floor(Math.random() * this.images.length)];
    this.currentImage = '/assets/animations/loading/' + image;
  }
}
