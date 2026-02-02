import { motion } from "framer-motion";
import { Heart, Twitter, Linkedin, Github } from "lucide-react";

const footerLinks = {
  Product: ["Features", "Pricing", "Security", "Integrations"],
  Company: ["About", "Blog", "Careers", "Press"],
  Resources: ["Documentation", "Help Center", "API Reference", "Status"],
  Legal: ["Privacy", "Terms", "HIPAA", "Cookie Policy"],
};

const Footer = () => {
  return (
    <footer className="relative border-t border-border bg-surface">
      <div className="container-clinical py-16 md:py-20">
        {/* Main footer content */}
        <div className="grid grid-cols-2 md:grid-cols-6 gap-8 mb-12">
          {/* Brand column */}
          <div className="col-span-2">
            <div className="flex items-center gap-2 mb-4">
              <div className="w-10 h-10 rounded-xl bg-cta flex items-center justify-center shadow-glow-sm">
                <Heart className="w-5 h-5 text-cta-foreground" />
              </div>
              <span className="font-display text-xl font-bold text-foreground">
                Greens Health
              </span>
            </div>
            <p className="text-muted-foreground text-sm leading-relaxed mb-6 max-w-xs">
              Pioneering predictive cardiovascular health through AI-powered
              digital twin technology.
            </p>
            {/* Social links */}
            <div className="flex items-center gap-3">
              {[Twitter, Linkedin, Github].map((Icon, index) => (
                <a
                  key={index}
                  href="#"
                  className="w-10 h-10 rounded-lg bg-primary/30 border border-border flex items-center justify-center text-muted-foreground hover:text-glow hover:border-glow/30 transition-all duration-hover"
                  aria-label={`Social link ${index + 1}`}
                >
                  <Icon className="w-4 h-4" />
                </a>
              ))}
            </div>
          </div>

          {/* Link columns */}
          {Object.entries(footerLinks).map(([category, links]) => (
            <div key={category}>
              <h4 className="font-display font-semibold text-foreground mb-4">
                {category}
              </h4>
              <ul className="space-y-3">
                {links.map((link) => (
                  <li key={link}>
                    <a
                      href="#"
                      className="text-sm text-muted-foreground hover:text-glow transition-colors duration-hover"
                    >
                      {link}
                    </a>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>

        {/* Bottom bar */}
        <div className="pt-8 border-t border-border flex flex-col md:flex-row items-center justify-between gap-4">
          <p className="text-sm text-muted-foreground">
            © {new Date().getFullYear()} Greens Health, Inc. All rights reserved.
          </p>
          <div className="flex items-center gap-2 text-sm text-muted-foreground">
            <span>Made with</span>
            <motion.span
              animate={{ scale: [1, 1.2, 1] }}
              transition={{ duration: 1, repeat: Infinity, repeatDelay: 2 }}
            >
              <Heart className="w-4 h-4 text-glow fill-glow" />
            </motion.span>
            <span>for better health</span>
          </div>
        </div>
      </div>
    </footer>
  );
};

export { Footer };
