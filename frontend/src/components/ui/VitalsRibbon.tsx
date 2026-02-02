import { useEffect, useRef } from "react";
import { cn } from "@/lib/utils";

interface VitalsRibbonProps {
  className?: string;
}

const VitalsRibbon = ({ className }: VitalsRibbonProps) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    // Check for reduced motion preference
    const prefersReducedMotion = window.matchMedia(
      "(prefers-reduced-motion: reduce)"
    ).matches;

    if (prefersReducedMotion) {
      // Draw static pattern
      drawStaticPattern(ctx, canvas.width, canvas.height);
      return;
    }

    let animationId: number;
    let time = 0;

    const resize = () => {
      const dpr = window.devicePixelRatio || 1;
      const rect = canvas.getBoundingClientRect();
      canvas.width = rect.width * dpr;
      canvas.height = rect.height * dpr;
      ctx.scale(dpr, dpr);
    };

    const drawWave = (
      yOffset: number,
      amplitude: number,
      frequency: number,
      phase: number,
      color: string,
      lineWidth: number
    ) => {
      const width = canvas.width / (window.devicePixelRatio || 1);
      const height = canvas.height / (window.devicePixelRatio || 1);

      ctx.beginPath();
      ctx.strokeStyle = color;
      ctx.lineWidth = lineWidth;

      for (let x = 0; x <= width; x += 2) {
        const y =
          height / 2 +
          yOffset +
          Math.sin((x * frequency) / 100 + phase + time * 0.02) * amplitude;
        
        if (x === 0) {
          ctx.moveTo(x, y);
        } else {
          ctx.lineTo(x, y);
        }
      }

      ctx.stroke();
    };

    const drawHeartbeat = (xOffset: number, yOffset: number, scale: number, opacity: number) => {
      const height = canvas.height / (window.devicePixelRatio || 1);
      const baseY = height / 2 + yOffset;
      
      ctx.beginPath();
      ctx.strokeStyle = `hsla(155, 65%, 36%, ${opacity})`;
      ctx.lineWidth = 2 * scale;
      ctx.lineCap = "round";
      ctx.lineJoin = "round";

      // Simplified ECG-like pattern
      const points = [
        [0, 0],
        [20, 0],
        [25, -5],
        [30, 0],
        [35, 0],
        [40, -40 * scale],
        [45, 30 * scale],
        [50, -10 * scale],
        [55, 0],
        [80, 0],
      ];

      const animOffset = (time * 0.5 + xOffset) % 200;

      points.forEach(([x, y], i) => {
        const px = x + animOffset;
        const py = baseY + y;
        if (i === 0) ctx.moveTo(px, py);
        else ctx.lineTo(px, py);
      });

      ctx.stroke();
    };

    const animate = () => {
      const width = canvas.width / (window.devicePixelRatio || 1);
      const height = canvas.height / (window.devicePixelRatio || 1);

      ctx.clearRect(0, 0, width, height);

      // Background waves
      drawWave(0, 30, 0.8, 0, "hsla(155, 65%, 36%, 0.08)", 1);
      drawWave(-20, 20, 1.2, Math.PI / 4, "hsla(160, 65%, 14%, 0.1)", 1);
      drawWave(20, 25, 0.6, Math.PI / 2, "hsla(155, 65%, 36%, 0.06)", 1);

      // Heartbeat lines
      for (let i = 0; i < 3; i++) {
        drawHeartbeat(i * 200, (i - 1) * 40, 0.8, 0.15 + i * 0.05);
      }

      time++;
      animationId = requestAnimationFrame(animate);
    };

    resize();
    window.addEventListener("resize", resize);
    animate();

    return () => {
      window.removeEventListener("resize", resize);
      cancelAnimationFrame(animationId);
    };
  }, []);

  return (
    <canvas
      ref={canvasRef}
      className={cn(
        "absolute inset-0 w-full h-full pointer-events-none opacity-60",
        className
      )}
    />
  );
};

const drawStaticPattern = (
  ctx: CanvasRenderingContext2D,
  width: number,
  height: number
) => {
  ctx.strokeStyle = "hsla(155, 65%, 36%, 0.1)";
  ctx.lineWidth = 1;

  // Draw a simple static wave
  ctx.beginPath();
  for (let x = 0; x <= width; x += 2) {
    const y = height / 2 + Math.sin(x * 0.01) * 20;
    if (x === 0) ctx.moveTo(x, y);
    else ctx.lineTo(x, y);
  }
  ctx.stroke();
};

export { VitalsRibbon };
