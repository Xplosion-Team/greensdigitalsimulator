import { motion } from "framer-motion";
import { cn } from "@/lib/utils";
import { LucideIcon } from "lucide-react";

interface FeatureCardProps {
  icon: LucideIcon;
  title: string;
  description: string;
  className?: string;
  index?: number;
}

const FeatureCard = ({
  icon: Icon,
  title,
  description,
  className,
  index = 0,
}: FeatureCardProps) => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 30 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: "-50px" }}
      transition={{
        duration: 0.6,
        delay: index * 0.1,
        ease: [0.22, 1, 0.36, 1],
      }}
      className={cn(
        "clinical-card group relative overflow-hidden transition-all duration-ui ease-cinematic hover:shadow-clinical-hover hover:border-glow/30",
        className
      )}
    >
      {/* Subtle gradient on hover */}
      <div className="absolute inset-0 bg-gradient-to-br from-glow/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-ui" />
      
      <div className="relative z-10">
        <div className="w-12 h-12 rounded-xl bg-primary/50 flex items-center justify-center mb-5 group-hover:bg-cta/50 transition-colors duration-ui">
          <Icon className="w-6 h-6 text-glow" />
        </div>
        
        <h3 className="font-display text-xl font-semibold text-foreground mb-3">
          {title}
        </h3>
        
        <p className="text-muted-foreground leading-relaxed">
          {description}
        </p>
      </div>
    </motion.div>
  );
};

export { FeatureCard };
