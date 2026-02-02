import { useEffect, useRef } from "react";
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { cn } from "@/lib/utils";
import { Camera, Brain, Zap } from "lucide-react";

gsap.registerPlugin(ScrollTrigger);

interface StoryBeat {
  icon: React.ComponentType<{ className?: string }>;
  title: string;
  subtitle: string;
  description: string;
}

const storyBeats: StoryBeat[] = [
  {
    icon: Camera,
    title: "Capture",
    subtitle: "Every reading, every moment",
    description:
      "Seamlessly log blood pressure readings through our intuitive interface. Manual entry or connected devices—your data flows effortlessly into your personal health timeline.",
  },
  {
    icon: Brain,
    title: "Understand",
    subtitle: "AI-powered pattern recognition",
    description:
      "Our digital twin analyzes your readings alongside lifestyle factors, medications, and environmental data to reveal hidden patterns and predict trends before they emerge.",
  },
  {
    icon: Zap,
    title: "Act",
    subtitle: "Personalized interventions",
    description:
      "Receive timely, actionable insights tailored to your unique physiology. Know when to rest, when to move, and how small changes create lasting impact.",
  },
];

const ScrollStory = () => {
  const containerRef = useRef<HTMLDivElement>(null);
  const storyRef = useRef<HTMLDivElement>(null);
  const beatsRef = useRef<(HTMLDivElement | null)[]>([]);

  useEffect(() => {
    // Check for reduced motion preference
    const prefersReducedMotion = window.matchMedia(
      "(prefers-reduced-motion: reduce)"
    ).matches;

    if (prefersReducedMotion) return;

    const container = containerRef.current;
    const story = storyRef.current;
    if (!container || !story) return;

    const ctx = gsap.context(() => {
      // Pin the container
      ScrollTrigger.create({
        trigger: container,
        start: "top top",
        end: `+=${window.innerHeight * 3}`,
        pin: story,
        pinSpacing: true,
      });

      // Animate each beat
      beatsRef.current.forEach((beat, index) => {
        if (!beat) return;

        const startProgress = index / storyBeats.length;
        const endProgress = (index + 1) / storyBeats.length;

        gsap.set(beat, { opacity: 0, scale: 0.95, y: 30 });

        ScrollTrigger.create({
          trigger: container,
          start: "top top",
          end: `+=${window.innerHeight * 3}`,
          scrub: 0.5,
          onUpdate: (self) => {
            const progress = self.progress;
            
            // Fade in
            if (progress >= startProgress && progress < endProgress) {
              const localProgress = (progress - startProgress) / (endProgress - startProgress);
              const fadeIn = Math.min(localProgress * 3, 1);
              const fadeOut = localProgress > 0.7 ? 1 - (localProgress - 0.7) / 0.3 : 1;
              const opacity = index === storyBeats.length - 1 ? fadeIn : fadeIn * fadeOut;
              
              gsap.to(beat, {
                opacity,
                scale: 0.95 + fadeIn * 0.05,
                y: 30 - fadeIn * 30,
                duration: 0.1,
                ease: "power2.out",
              });
            } else if (progress < startProgress) {
              gsap.to(beat, { opacity: 0, scale: 0.95, y: 30, duration: 0.1 });
            }
          },
        });
      });
    }, container);

    return () => ctx.revert();
  }, []);

  return (
    <section
      ref={containerRef}
      className="relative bg-background"
      aria-label="How it works"
    >
      <div
        ref={storyRef}
        className="h-screen flex items-center justify-center"
      >
        <div className="container-clinical relative w-full">
          {/* Background decoration */}
          <div className="absolute inset-0 -z-10">
            <div className="gradient-blob gradient-blob-primary w-[600px] h-[600px] -top-40 -left-40" />
            <div className="gradient-blob gradient-blob-accent w-[400px] h-[400px] -bottom-20 -right-20" />
          </div>

          {/* Story content */}
          <div className="relative w-full text-center">
            {storyBeats.map((beat, index) => {
              const Icon = beat.icon;
              return (
                <div
                  key={beat.title}
                  ref={(el) => (beatsRef.current[index] = el)}
                  className={cn(
                    "absolute inset-0 flex flex-col items-center justify-center",
                    index === 0 && "opacity-100"
                  )}
                >
                  {/* Icon */}
                  <div className="w-16 h-16 md:w-20 md:h-20 lg:w-24 lg:h-24 rounded-2xl bg-primary/50 border border-border flex items-center justify-center mb-6 md:mb-8 lg:mb-10 shadow-glow-sm">
                    <Icon className="w-8 h-8 md:w-10 md:h-10 lg:w-12 lg:h-12 text-glow" />
                  </div>

                  {/* Step indicator */}
                  <div className="flex items-center gap-2 md:gap-3 lg:gap-4 mb-3 md:mb-4 lg:mb-6">
                    <span className="text-glow font-display text-xs md:text-sm font-semibold uppercase tracking-widest">
                      Step {index + 1}
                    </span>
                    <div className="w-8 md:w-12 lg:w-16 h-px bg-glow/30" />
                  </div>

                  {/* Title */}
                  <h3 className="font-display text-3xl md:text-5xl lg:text-6xl font-bold text-foreground mb-4 md:mb-6 lg:mb-8 text-glow">
                    {beat.title}
                  </h3>

                  {/* Subtitle */}
                  <p className="text-glow/80 text-base md:text-xl lg:text-2xl font-medium mb-4 md:mb-6 lg:mb-8">
                    {beat.subtitle}
                  </p>

                  {/* Description */}
                  <p className="text-muted-foreground text-sm md:text-base lg:text-lg max-w-xl md:max-w-3xl lg:max-w-4xl leading-relaxed px-4">
                    {beat.description}
                  </p>
                </div>
              );
            })}
          </div>

          {/* Progress indicator */}
          <div className="absolute bottom-12 left-1/2 -translate-x-1/2 flex gap-3">
            {storyBeats.map((_, index) => (
              <div
                key={index}
                className="w-2 h-2 rounded-full bg-muted transition-colors duration-ui"
              />
            ))}
          </div>
        </div>
      </div>
    </section>
  );
};

export { ScrollStory };
