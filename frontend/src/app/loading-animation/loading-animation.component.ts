import { Component, OnInit } from '@angular/core';
import { LoadingAnimationService } from '../loading-animation.service';

@Component({
    selector: 'app-loading-animation',
    templateUrl: './loading-animation.component.html',
    styleUrls: ['./loading-animation.component.css']
})
export class LoadingAnimationComponent implements OnInit {
    isVisible = false;
    public get animationImagePath(): string {
        return this.loadingAnimationService.getImagePath();
    }
    constructor(private loadingAnimationService: LoadingAnimationService) { }
    ngOnInit() {
        const self = this;
        this.loadingAnimationService.runningChanged.subscribe((isRunning) => {
            if (isRunning) {
                self.isVisible = true;
            } else {
                if (self.isVisible) {
                    setTimeout(() => {
                        self.isVisible = false;
                        self.loadingAnimationService.changeImage();
                    }, 800);
                }
            }
        });
    }
}
