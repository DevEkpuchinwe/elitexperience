import { useState } from "react";
import { useParams, Link } from "react-router";
import { celebData, services } from "../data/celebData";
import { motion } from "motion/react";
import { ArrowLeft, Sparkles, Heart, Check } from "lucide-react";
import { Button } from "../components/ui/button";
import { Input } from "../components/ui/input";
import { Textarea } from "../components/ui/textarea";
import { Checkbox } from "../components/ui/checkbox";
import { Label } from "../components/ui/label";
import { toast } from "sonner";

export function BookingPage() {
  const { celebName } = useParams();
  const celeb = celebData[celebName || ""] || celebData["default"];
  
  const [formData, setFormData] = useState({
    name: "",
    country: "",
    address: "",
    phone: "",
    email: "",
    selectedServices: [] as string[],
    message: "",
    occupation: "",
    age: ""
  });

  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleServiceToggle = (serviceId: string) => {
    if (serviceId === "all") {
      if (formData.selectedServices.includes("all")) {
        setFormData({ ...formData, selectedServices: [] });
      } else {
        setFormData({ ...formData, selectedServices: ["all", ...services.map(s => s.id)] });
      }
    } else {
      const newServices = formData.selectedServices.includes(serviceId)
        ? formData.selectedServices.filter(s => s !== serviceId && s !== "all")
        : [...formData.selectedServices.filter(s => s !== "all"), serviceId];
      setFormData({ ...formData, selectedServices: newServices });
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!formData.name || !formData.email || !formData.phone || formData.selectedServices.length === 0) {
      toast.error("Please fill in all required fields");
      return;
    }

    setIsSubmitting(true);

    // Simulate submission - in real app, this would save to database
    setTimeout(() => {
      console.log("Form submitted:", formData);
      toast.success("Your booking request has been submitted! We'll contact you within 24 hours.");
      setIsSubmitting(false);
      
      // Reset form
      setFormData({
        name: "",
        country: "",
        address: "",
        phone: "",
        email: "",
        selectedServices: [],
        message: "",
        occupation: "",
        age: ""
      });
    }, 1500);
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-black via-purple-950/30 to-black text-white">
      {/* Header */}
      <header className="border-b border-white/10 bg-black/80 backdrop-blur-lg">
        <div className="container mx-auto px-4 py-4">
          <Link to={`/${celebName}`} className="flex items-center gap-2 hover:text-purple-400 transition-colors w-fit">
            <ArrowLeft className="w-5 h-5" />
            <span>Back to {celeb.name}</span>
          </Link>
        </div>
      </header>

      <div className="container mx-auto px-4 py-16 max-w-3xl">
        {/* Hero Text */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-12"
        >
          <div className="inline-block bg-gradient-to-r from-purple-600 to-pink-600 p-3 rounded-full mb-6">
            <Heart className="w-12 h-12" />
          </div>
          <h1 className="text-4xl md:text-5xl mb-4">
            Want To Have Your Personal Moment With{" "}
            <span className="bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent">
              {celeb.name}
            </span>
            ?
          </h1>
          <p className="text-xl text-white/80 mb-4">
            You're just one step away from an unforgettable experience!
          </p>
          <p className="text-white/70">
            Fill out the form below and our team will personally coordinate everything for you. 
            Limited slots available - don't miss this exclusive opportunity!
          </p>
        </motion.div>

        {/* Booking Form */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="bg-white/5 backdrop-blur-xl border border-white/10 rounded-3xl p-8 md:p-12 shadow-2xl"
        >
          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Name */}
            <div>
              <Label htmlFor="name" className="text-white mb-2 block">
                Full Name <span className="text-red-400">*</span>
              </Label>
              <Input
                id="name"
                required
                value={formData.name}
                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                className="bg-white/10 border-white/20 text-white placeholder:text-white/50"
                placeholder="Enter your full name"
              />
            </div>

            {/* Country & Address */}
            <div className="grid md:grid-cols-2 gap-4">
              <div>
                <Label htmlFor="country" className="text-white mb-2 block">
                  Country <span className="text-red-400">*</span>
                </Label>
                <Input
                  id="country"
                  required
                  value={formData.country}
                  onChange={(e) => setFormData({ ...formData, country: e.target.value })}
                  className="bg-white/10 border-white/20 text-white placeholder:text-white/50"
                  placeholder="Your country"
                />
              </div>
              <div>
                <Label htmlFor="address" className="text-white mb-2 block">
                  City/Address <span className="text-red-400">*</span>
                </Label>
                <Input
                  id="address"
                  required
                  value={formData.address}
                  onChange={(e) => setFormData({ ...formData, address: e.target.value })}
                  className="bg-white/10 border-white/20 text-white placeholder:text-white/50"
                  placeholder="City or address"
                />
              </div>
            </div>

            {/* Phone & Email */}
            <div className="grid md:grid-cols-2 gap-4">
              <div>
                <Label htmlFor="phone" className="text-white mb-2 block">
                  Phone Number <span className="text-red-400">*</span>
                </Label>
                <Input
                  id="phone"
                  type="tel"
                  required
                  value={formData.phone}
                  onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
                  className="bg-white/10 border-white/20 text-white placeholder:text-white/50"
                  placeholder="WhatsApp preferred"
                />
                <p className="text-xs text-white/50 mt-1">WhatsApp preferred for faster communication</p>
              </div>
              <div>
                <Label htmlFor="email" className="text-white mb-2 block">
                  Email Address <span className="text-red-400">*</span>
                </Label>
                <Input
                  id="email"
                  type="email"
                  required
                  value={formData.email}
                  onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                  className="bg-white/10 border-white/20 text-white placeholder:text-white/50"
                  placeholder="your@email.com"
                />
              </div>
            </div>

            {/* Services Selection */}
            <div>
              <Label className="text-white mb-3 block">
                What Are You Interested In? <span className="text-red-400">*</span>
              </Label>
              <div className="space-y-3 bg-white/5 border border-white/10 rounded-xl p-4">
                {/* All Services Option */}
                <div className="flex items-start gap-3 p-3 rounded-lg hover:bg-white/5 transition-colors">
                  <Checkbox
                    id="service-all"
                    checked={formData.selectedServices.includes("all")}
                    onCheckedChange={() => handleServiceToggle("all")}
                    className="mt-0.5"
                  />
                  <Label htmlFor="service-all" className="cursor-pointer flex-1">
                    <div className="flex items-center gap-2">
                      <Sparkles className="w-4 h-4 text-purple-400" />
                      <span className="text-white">All Services (Best Value!)</span>
                    </div>
                    <p className="text-xs text-white/60 mt-1">Get the complete VIP experience</p>
                  </Label>
                </div>

                <div className="border-t border-white/10 pt-3">
                  {services.map((service) => (
                    <div key={service.id} className="flex items-start gap-3 p-3 rounded-lg hover:bg-white/5 transition-colors">
                      <Checkbox
                        id={`service-${service.id}`}
                        checked={formData.selectedServices.includes(service.id) || formData.selectedServices.includes("all")}
                        onCheckedChange={() => handleServiceToggle(service.id)}
                        className="mt-0.5"
                        disabled={formData.selectedServices.includes("all")}
                      />
                      <Label htmlFor={`service-${service.id}`} className="cursor-pointer flex-1">
                        <div className="text-white">{service.name}</div>
                        <p className="text-xs text-white/60 mt-1">{service.description}</p>
                      </Label>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            {/* Occupation & Age */}
            <div className="grid md:grid-cols-2 gap-4">
              <div>
                <Label htmlFor="occupation" className="text-white mb-2 block">
                  Occupation
                </Label>
                <Input
                  id="occupation"
                  value={formData.occupation}
                  onChange={(e) => setFormData({ ...formData, occupation: e.target.value })}
                  className="bg-white/10 border-white/20 text-white placeholder:text-white/50"
                  placeholder="Your occupation"
                />
              </div>
              <div>
                <Label htmlFor="age" className="text-white mb-2 block">
                  Age
                </Label>
                <Input
                  id="age"
                  value={formData.age}
                  onChange={(e) => setFormData({ ...formData, age: e.target.value })}
                  className="bg-white/10 border-white/20 text-white placeholder:text-white/50"
                  placeholder="Your age"
                />
              </div>
            </div>

            {/* Message */}
            <div>
              <Label htmlFor="message" className="text-white mb-2 block">
                Short Message to {celeb.name} <span className="text-white/50">(Optional)</span>
              </Label>
              <Textarea
                id="message"
                value={formData.message}
                onChange={(e) => setFormData({ ...formData, message: e.target.value })}
                className="bg-white/10 border-white/20 text-white placeholder:text-white/50 min-h-[120px]"
                placeholder="Share your thoughts, why you'd love to meet, or any special requests..."
              />
            </div>

            {/* Submit Button */}
            <Button
              type="submit"
              size="lg"
              disabled={isSubmitting}
              className="w-full bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-lg py-6"
            >
              {isSubmitting ? (
                "Submitting..."
              ) : (
                <>
                  <Check className="w-5 h-5 mr-2" />
                  Submit Booking Request
                </>
              )}
            </Button>

            <p className="text-center text-sm text-white/60 mt-4">
              By submitting this form, you agree to be contacted by our team via email, phone, or WhatsApp
              regarding your booking request. We typically respond within 24 hours.
            </p>
          </form>
        </motion.div>

        {/* Additional Info */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.4 }}
          className="mt-8 text-center space-y-4 text-white/60"
        >
          <p className="flex items-center justify-center gap-2">
            <Check className="w-4 h-4 text-green-400" />
            <span>100% Secure & Confidential</span>
          </p>
          <p className="flex items-center justify-center gap-2">
            <Check className="w-4 h-4 text-green-400" />
            <span>Official {celeb.management} Authorized</span>
          </p>
          <p className="flex items-center justify-center gap-2">
            <Check className="w-4 h-4 text-green-400" />
            <span>No Hidden Fees</span>
          </p>
        </motion.div>
      </div>
    </div>
  );
}
