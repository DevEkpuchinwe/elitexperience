import { useParams, useNavigate, Link } from "react-router";
import { celebData } from "../data/celebData";
import { motion } from "motion/react";
import { 
  Star, Shield, Award, Users, Ticket, Camera, Clock, 
  CheckCircle, MapPin, Car, Lock, Calendar, MessageCircle,
  Sparkles, Heart, TrendingUp, Gift
} from "lucide-react";
import { Button } from "../components/ui/button";

export function CelebPage() {
  const { celebName } = useParams();
  const navigate = useNavigate();
  
  const celeb = celebData[celebName || ""] || celebData["default"];

  const scrollToSection = (id: string) => {
    const element = document.getElementById(id);
    if (element) {
      element.scrollIntoView({ behavior: "smooth" });
    }
  };

  return (
    <div className="min-h-screen bg-black text-white">
      {/* Header */}
      <header className="fixed top-0 left-0 right-0 z-50 bg-black/80 backdrop-blur-lg border-b border-white/10">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <h1 className="text-2xl">{celeb.name}</h1>
          <nav className="hidden md:flex gap-6">
            <button onClick={() => scrollToSection("benefits")} className="hover:text-purple-400 transition-colors">Benefits</button>
            <button onClick={() => scrollToSection("meeting")} className="hover:text-purple-400 transition-colors">What to Expect</button>
            <button onClick={() => scrollToSection("about")} className="hover:text-purple-400 transition-colors">About</button>
            <button onClick={() => scrollToSection("services")} className="hover:text-purple-400 transition-colors">Services</button>
            <button onClick={() => scrollToSection("photos")} className="hover:text-purple-400 transition-colors">Gallery</button>
            <button onClick={() => scrollToSection("process")} className="hover:text-purple-400 transition-colors">Process</button>
          </nav>
          <Link to={`/${celebName}/book`}>
            <Button className="bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700">
              Book Now
            </Button>
          </Link>
        </div>
      </header>

      {/* Hero Section with Glass Effect */}
      <section 
        className="relative h-screen flex items-center justify-center"
        style={{
          backgroundImage: `url(${celeb.heroImage})`,
          backgroundSize: 'cover',
          backgroundPosition: 'center'
        }}
      >
        <div className="absolute inset-0 bg-black/50" />
        <div className="absolute inset-0 backdrop-blur-sm" />
        
        <motion.div 
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="relative z-10 max-w-4xl mx-auto px-4 text-center"
        >
          <div className="bg-white/10 backdrop-blur-xl border border-white/20 rounded-3xl p-12 shadow-2xl">
            <h2 className="text-5xl md:text-7xl mb-6 bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent">
              {celeb.tagline}
            </h2>
            <p className="text-xl md:text-2xl mb-8 text-white/90">
              {celeb.heroText}
            </p>
            
            {/* Stats */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
              <div className="bg-white/5 backdrop-blur-sm rounded-xl p-4 border border-white/10">
                <div className="text-3xl text-purple-400">{celeb.stats.meetGreets}+</div>
                <div className="text-sm text-white/70">Meet & Greets</div>
              </div>
              <div className="bg-white/5 backdrop-blur-sm rounded-xl p-4 border border-white/10">
                <div className="text-3xl text-pink-400">{celeb.stats.privateTime}+</div>
                <div className="text-sm text-white/70">Private Sessions</div>
              </div>
              <div className="bg-white/5 backdrop-blur-sm rounded-xl p-4 border border-white/10">
                <div className="text-3xl text-blue-400">{celeb.stats.ticketsSold}+</div>
                <div className="text-sm text-white/70">Tickets Sold</div>
              </div>
              <div className="bg-white/5 backdrop-blur-sm rounded-xl p-4 border border-white/10">
                <div className="text-3xl text-green-400">{celeb.stats.fanCards}+</div>
                <div className="text-sm text-white/70">Fan Cards</div>
              </div>
            </div>

            <div className="flex items-center justify-center gap-2 mb-8 text-white/80">
              <Shield className="w-5 h-5 text-green-400" />
              <span>Authorized by {celeb.management}</span>
            </div>

            <Link to={`/${celebName}/book`}>
              <Button size="lg" className="bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-lg px-8 py-6">
                <Sparkles className="w-5 h-5 mr-2" />
                Book Your Exclusive Experience
              </Button>
            </Link>
          </div>
        </motion.div>
      </section>

      {/* Benefits Section */}
      <section id="benefits" className="py-20 bg-gradient-to-b from-black to-purple-950/20">
        <div className="container mx-auto px-4">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl md:text-5xl mb-4">Why Book With Us?</h2>
            <p className="text-xl text-white/70">Direct access, verified experiences, unforgettable memories</p>
          </motion.div>

          <div className="grid md:grid-cols-3 gap-8">
            {[
              {
                icon: <Shield className="w-12 h-12 text-purple-400" />,
                title: "100% Verified & Authorized",
                description: "All bookings are officially verified by celebrity management teams"
              },
              {
                icon: <Star className="w-12 h-12 text-yellow-400" />,
                title: "Exclusive Direct Access",
                description: "Skip the middlemen - book directly with official representatives"
              },
              {
                icon: <Award className="w-12 h-12 text-blue-400" />,
                title: "Premium Experience",
                description: "VIP treatment with luxury accommodations and top-tier service"
              },
              {
                icon: <Lock className="w-12 h-12 text-green-400" />,
                title: "Privacy & Security",
                description: "Your information is protected with bank-level encryption"
              },
              {
                icon: <Users className="w-12 h-12 text-pink-400" />,
                title: "Personal Coordination",
                description: "Dedicated team member to handle all your arrangements"
              },
              {
                icon: <TrendingUp className="w-12 h-12 text-orange-400" />,
                title: "Best Value Guarantee",
                description: "Competitive pricing with no hidden fees or charges"
              }
            ].map((benefit, i) => (
              <motion.div
                key={i}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.1 }}
                className="bg-white/5 backdrop-blur-sm border border-white/10 rounded-2xl p-8 hover:bg-white/10 transition-all"
              >
                <div className="mb-4">{benefit.icon}</div>
                <h3 className="text-xl mb-3">{benefit.title}</h3>
                <p className="text-white/70">{benefit.description}</p>
              </motion.div>
            ))}
          </div>

          <div className="text-center mt-12">
            <Link to={`/${celebName}/book`}>
              <Button size="lg" className="bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700">
                Get Started Now
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* Meeting & What to Expect Section */}
      <section id="meeting" className="py-20 bg-gradient-to-b from-purple-950/20 to-black">
        <div className="container mx-auto px-4">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl md:text-5xl mb-4">What to Expect</h2>
            <p className="text-xl text-white/70">We handle everything so you can focus on the experience</p>
          </motion.div>

          <div className="grid md:grid-cols-2 gap-12 items-center">
            <motion.div
              initial={{ opacity: 0, x: -30 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
            >
              <img 
                src="https://images.unsplash.com/photo-1761110787206-2cc164e4913c?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxsdXh1cnklMjBldmVudCUyMHZlbnVlfGVufDF8fHx8MTc3NTM5Njk0M3ww&ixlib=rb-4.1.0&q=80&w=1080"
                alt="Luxury experience"
                className="rounded-2xl shadow-2xl"
              />
            </motion.div>

            <motion.div
              initial={{ opacity: 0, x: 30 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
              className="space-y-6"
            >
              {[
                { icon: <Car className="w-8 h-8" />, title: "Premium Transportation", desc: "Luxury vehicle pickup and drop-off" },
                { icon: <MapPin className="w-8 h-8" />, title: "Venue Logistics", desc: "All location arrangements handled for you" },
                { icon: <Shield className="w-8 h-8" />, title: "Professional Security", desc: "Trained security personnel for your safety" },
                { icon: <Gift className="w-8 h-8" />, title: "Welcome Package", desc: "Exclusive merchandise and memorabilia" },
                { icon: <Camera className="w-8 h-8" />, title: "Photo Opportunities", desc: "Professional photography included" },
                { icon: <Heart className="w-8 h-8" />, title: "Memorable Experience", desc: "Create moments that last a lifetime" }
              ].map((item, i) => (
                <div key={i} className="flex items-start gap-4 bg-white/5 backdrop-blur-sm border border-white/10 rounded-xl p-4">
                  <div className="text-purple-400">{item.icon}</div>
                  <div>
                    <h3 className="text-lg mb-1">{item.title}</h3>
                    <p className="text-white/70 text-sm">{item.desc}</p>
                  </div>
                </div>
              ))}
            </motion.div>
          </div>

          <div className="text-center mt-12">
            <Link to={`/${celebName}/book`}>
              <Button size="lg" className="bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700">
                <Clock className="w-5 h-5 mr-2" />
                Book Your Spot Now
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* Get to Know Section */}
      <section id="about" className="py-20 bg-gradient-to-b from-black to-blue-950/20">
        <div className="container mx-auto px-4">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="max-w-3xl mx-auto text-center mb-12"
          >
            <h2 className="text-4xl md:text-5xl mb-6">Get to Know {celeb.name}</h2>
            <p className="text-lg text-white/80 mb-8">{celeb.bio}</p>
            
            <div className="flex flex-wrap justify-center gap-3 mb-8">
              {celeb.interests.map((interest, i) => (
                <span key={i} className="bg-purple-600/20 border border-purple-400/30 px-4 py-2 rounded-full text-purple-300">
                  {interest}
                </span>
              ))}
            </div>
          </motion.div>
        </div>
      </section>

      {/* Services Section */}
      <section id="services" className="py-20 bg-gradient-to-b from-blue-950/20 to-black">
        <div className="container mx-auto px-4">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl md:text-5xl mb-4">What We Offer</h2>
            <p className="text-xl text-white/70">Choose from our exclusive range of experiences</p>
          </motion.div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {[
              { icon: <Award />, title: "Official Fan Card", desc: "Exclusive verified fan card with special perks and benefits" },
              { icon: <Users />, title: "Meet & Greet", desc: "Personal meet and greet session with photo opportunities" },
              { icon: <Ticket />, title: "Concert Tickets", desc: "Premium tickets to upcoming shows and events" },
              { icon: <Star />, title: "Premium VIP Seats", desc: "Front row and VIP seating arrangements" },
              { icon: <Sparkles />, title: "After Event Meet-up", desc: "Exclusive backstage access after the show" },
              { icon: <Camera />, title: "Photo Session", desc: "Professional photo opportunity with the celebrity" },
              { icon: <Heart />, title: "Private Time Together", desc: "One-on-one exclusive time with your favorite star" }
            ].map((service, i) => (
              <motion.div
                key={i}
                initial={{ opacity: 0, scale: 0.9 }}
                whileInView={{ opacity: 1, scale: 1 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.05 }}
                className="bg-gradient-to-br from-purple-900/20 to-pink-900/20 border border-purple-500/30 rounded-2xl p-6 hover:border-purple-400/50 transition-all"
              >
                <div className="text-purple-400 mb-4">{service.icon}</div>
                <h3 className="text-xl mb-2">{service.title}</h3>
                <p className="text-white/70 text-sm">{service.desc}</p>
              </motion.div>
            ))}
          </div>

          <div className="text-center mt-12">
            <Link to={`/${celebName}/book`}>
              <Button size="lg" className="bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700">
                Explore All Services
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* Photos Gallery */}
      <section id="photos" className="py-20 bg-black">
        <div className="container mx-auto px-4">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl md:text-5xl mb-4">Gallery</h2>
            <p className="text-xl text-white/70">Moments from previous experiences</p>
          </motion.div>

          <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
            {celeb.photos.map((photo, i) => (
              <motion.div
                key={i}
                initial={{ opacity: 0, scale: 0.8 }}
                whileInView={{ opacity: 1, scale: 1 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.1 }}
                className="relative aspect-square rounded-xl overflow-hidden group cursor-pointer"
              >
                <img 
                  src={photo} 
                  alt={`Gallery ${i + 1}`}
                  className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500"
                />
                <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent opacity-0 group-hover:opacity-100 transition-opacity" />
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Process Section */}
      <section id="process" className="py-20 bg-gradient-to-b from-black to-purple-950/20">
        <div className="container mx-auto px-4">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl md:text-5xl mb-4">How It Works</h2>
            <p className="text-xl text-white/70">Simple, secure, and seamless booking process</p>
          </motion.div>

          <div className="max-w-4xl mx-auto space-y-8">
            {[
              { step: "01", title: "Submit Your Details", desc: "Fill out the booking form with your preferences and information", icon: <MessageCircle /> },
              { step: "02", title: "Schedule Coordination", desc: "We add your request to the celebrity's schedule and confirm availability", icon: <Calendar /> },
              { step: "03", title: "Arrangements & Logistics", desc: "Our team handles all logistics, transportation, and venue arrangements", icon: <MapPin /> },
              { step: "04", title: "Security & Preparation", desc: "Professional security and all necessary preparations are put in place", icon: <Shield /> },
              { step: "05", title: "Experience Day", desc: "We connect you with the celebrity and ensure everything goes perfectly", icon: <Star /> },
              { step: "06", title: "Follow-up", desc: "Post-event support and ensuring your experience exceeded expectations", icon: <CheckCircle /> }
            ].map((step, i) => (
              <motion.div
                key={i}
                initial={{ opacity: 0, x: -30 }}
                whileInView={{ opacity: 1, x: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.1 }}
                className="flex items-start gap-6 bg-white/5 backdrop-blur-sm border border-white/10 rounded-2xl p-6"
              >
                <div className="flex-shrink-0">
                  <div className="w-16 h-16 rounded-full bg-gradient-to-br from-purple-600 to-pink-600 flex items-center justify-center text-2xl">
                    {step.step}
                  </div>
                </div>
                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-2">
                    <div className="text-purple-400">{step.icon}</div>
                    <h3 className="text-xl">{step.title}</h3>
                  </div>
                  <p className="text-white/70">{step.desc}</p>
                </div>
              </motion.div>
            ))}
          </div>

          <div className="text-center mt-12">
            <Link to={`/${celebName}/book`}>
              <Button size="lg" className="bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-lg px-10 py-6">
                <Sparkles className="w-5 h-5 mr-2" />
                Start Your Booking Journey
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-12 bg-black border-t border-white/10">
        <div className="container mx-auto px-4 text-center text-white/60">
          <p>© 2026 {celeb.name} Official Booking. Authorized by {celeb.management}</p>
          <p className="mt-2 text-sm">All experiences are verified and managed by official representatives</p>
        </div>
      </footer>
    </div>
  );
}
