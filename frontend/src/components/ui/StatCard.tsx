import { useEffect, useRef, useState } from "react";
import { motion, useInView } from "framer-motion";
import { cn } from "@/lib/utils";

interface StatCardProps {
  value: number;
  suffix?: string;
  prefix?: string;
  label: string;
  duration?: number;
  className?: string;
}

const StatCard = ({
  value,
  suffix = "",
  prefix = "",
  label,
  duration = 2000,
  className,
}: StatCardProps) => {
  const [count, setCount] = useState(0);
  const ref = useRef<HTMLDivElement>(null);
  const isInView = useInView(ref, { once: true, margin: "-100px" });

  useEffect(() => {
    if (!isInView) return;

    const startTime = Date.now();
    const endValue = value;

    const animate = () => {
      const now = Date.now();
      const elapsed = now - startTime;
      const progress = Math.min(elapsed / duration, 1);
      
      // Ease out cubic
      const eased = 1 - Math.pow(1 - progress, 3);
      const current = Math.floor(eased * endValue);
      
      setCount(current);

      if (progress < 1) {
        requestAnimationFrame(animate);
      }
    };

    requestAnimationFrame(animate);
  }, [isInView, value, duration]);

  return (
    <motion.div
      ref={ref}
      initial={{ opacity: 0, y: 20 }}
      animate={isInView ? { opacity: 1, y: 0 } : {}}
      transition={{ duration: 0.6, ease: [0.22, 1, 0.36, 1] }}
      className={cn(
        "flex flex-col items-center text-center p-6",
        className
      )}
    >
      <span className="font-display text-4xl md:text-5xl lg:text-6xl font-bold text-glow text-glow tracking-tight">
        {prefix}{count.toLocaleString()}{suffix}
      </span>
      <span className="mt-2 text-sm md:text-base text-muted-foreground font-medium uppercase tracking-wider">
        {label}
      </span>
    </motion.div>
  );
};

export { StatCard };
