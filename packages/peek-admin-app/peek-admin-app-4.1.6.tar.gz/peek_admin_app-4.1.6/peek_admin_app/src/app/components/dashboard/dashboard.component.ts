
import { Component, OnInit, OnDestroy } from "@angular/core";
import { CommonModule } from "@angular/common";
import { NzGridModule } from "ng-zorro-antd/grid";
import { NzCardModule } from "ng-zorro-antd/card";
import { NzIconModule } from "ng-zorro-antd/icon";
import { DashboardStatsComponent } from "../dashboard-stats/dashboard-stats.component";

@Component({
  selector: "app-dashboard",
  templateUrl: "./dashboard.component.html",
  styleUrls: ["./dashboard.component.scss"],
  standalone: true,
  imports: [
    CommonModule,
    NzGridModule,
    NzCardModule,
    NzIconModule,
    DashboardStatsComponent
  ]
})
export class DashboardComponent implements OnInit, OnDestroy {
  private canvas!: HTMLCanvasElement;
  private context!: CanvasRenderingContext2D;
  private chars: string[] = 'ABCDEFGHIJKLMNOPQRSTUVXYZABCDEFGHIJKLMNOPQRSTUVXYZABCDEFGHIJKLMNOPQRSTUVXYZABCDEFGHIJKLMNOPQRSTUVXYZ'.split('');
  private fontSize = 10;
  private drops: number[] = [];
  private animationFrameId?: number;

  ngOnInit() {
    setTimeout(() => this.initMatrix(), 100);
  }

  ngOnDestroy() {
    if (this.animationFrameId) {
      cancelAnimationFrame(this.animationFrameId);
    }
  }

  private initMatrix() {
    this.canvas = document.getElementById('matrixCanvas') as HTMLCanvasElement;
    if (!this.canvas) return;

    this.context = this.canvas.getContext('2d') as CanvasRenderingContext2D;
    this.canvas.width = this.canvas.offsetWidth;
    this.canvas.height = this.canvas.offsetHeight;

    const columns = this.canvas.width / this.fontSize;
    this.drops = Array(Math.floor(columns)).fill(1);

    this.animate();
  }

  private animate() {
    this.context.fillStyle = 'rgba(0, 0, 0, 0.05)';
    this.context.fillRect(0, 0, this.canvas.width, this.canvas.height);

    this.context.fillStyle = '#0F0';
    this.context.font = this.fontSize + 'px monospace';

    for (let i = 0; i < this.drops.length; i++) {
      const text = this.chars[Math.floor(Math.random() * this.chars.length)];
      this.context.fillText(text, i * this.fontSize, this.drops[i] * this.fontSize);

      if (this.drops[i] * this.fontSize > this.canvas.height && Math.random() > 0.975) {
        this.drops[i] = 0;
      }

      this.drops[i]++;
    }

    this.animationFrameId = requestAnimationFrame(() => this.animate());
  }
}