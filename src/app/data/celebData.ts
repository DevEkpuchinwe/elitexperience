// Mock celebrity data - can be replaced with API or Supabase
export const celebData: Record<string, CelebData> = {
  "taylor-swift": {
    name: "Taylor Swift",
    management: "TN Management",
    tagline: "Your Dream Moment with Taylor",
    heroText: "Don't Miss Your Chance! Limited spots available for exclusive meet & greets, private time, and VIP experiences.",
    stats: {
      meetGreets: 1247,
      privateTime: 89,
      ticketsSold: 15420,
      fanCards: 3892
    },
    bio: "Taylor Swift is a global superstar known for her heartfelt songwriting and incredible performances. She loves connecting with fans, exploring new cities, and creating unforgettable moments.",
    interests: ["Songwriting", "Cats", "Baking", "Surprise Songs"],
    heroImage: "https://images.unsplash.com/photo-1772587023108-61e60c18537a?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxjb25jZXJ0JTIwc3RhZ2UlMjBwZXJmb3JtZXIlMjBzcG90bGlnaHR8ZW58MXx8fHwxNzc1Mzk2OTQxfDA&ixlib=rb-4.1.0&q=80&w=1080",
    photos: [
      "https://images.unsplash.com/photo-1772587023108-61e60c18537a?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxjb25jZXJ0JTIwc3RhZ2UlMjBwZXJmb3JtZXIlMjBzcG90bGlnaHR8ZW58MXx8fHwxNzc1Mzk2OTQxfDA&ixlib=rb-4.1.0&q=80&w=1080",
      "https://images.unsplash.com/photo-1765560008448-612e4b17877f?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxjZWxlYnJpdHklMjByZWQlMjBjYXJwZXQlMjBldmVudHxlbnwxfHx8fDE3NzUzOTY5NDJ8MA&ixlib=rb-4.1.0&q=80&w=1080",
      "https://images.unsplash.com/photo-1716187249622-4bd9ae36a24c?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxleGNsdXNpdmUlMjB2aXAlMjBiYWNrc3RhZ2V8ZW58MXx8fHwxNzc1Mzk2OTQyfDA&ixlib=rb-4.1.0&q=80&w=1080",
      "https://images.unsplash.com/photo-1741829186423-43f6fa5ac781?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxtZWV0JTIwYW5kJTIwZ3JlZXQlMjBmYW5zfGVufDF8fHx8MTc3NTM5Njk0Mnww&ixlib=rb-4.1.0&q=80&w=1080",
      "https://images.unsplash.com/photo-1761110787206-2cc164e4913c?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxsdXh1cnklMjBldmVudCUyMHZlbnVlfGVufDF8fHx8MTc3NTM5Njk0M3ww&ixlib=rb-4.1.0&q=80&w=1080",
      "https://images.unsplash.com/photo-1771402899438-55fd9b239c6f?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxwcm9mZXNzaW9uYWwlMjBzZWN1cml0eSUyMGd1YXJkc3xlbnwxfHx8fDE3NzUzOTY5NDN8MA&ixlib=rb-4.1.0&q=80&w=1080"
    ]
  },
  "default": {
    name: "Your Favorite Artist",
    management: "Elite Artist Management",
    tagline: "Exclusive Access to Your Favorite Stars",
    heroText: "Experience once-in-a-lifetime moments with top celebrities. Limited availability - Book now before spots fill up!",
    stats: {
      meetGreets: 500,
      privateTime: 50,
      ticketsSold: 10000,
      fanCards: 2000
    },
    bio: "Connect with your favorite celebrities through our exclusive booking platform. We specialize in creating unforgettable experiences.",
    interests: ["Music", "Fashion", "Travel", "Fans"],
    heroImage: "https://images.unsplash.com/photo-1772587023108-61e60c18537a?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxjb25jZXJ0JTIwc3RhZ2UlMjBwZXJmb3JtZXIlMjBzcG90bGlnaHR8ZW58MXx8fHwxNzc1Mzk2OTQxfDA&ixlib=rb-4.1.0&q=80&w=1080",
    photos: [
      "https://images.unsplash.com/photo-1772587023108-61e60c18537a?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxjb25jZXJ0JTIwc3RhZ2UlMjBwZXJmb3JtZXIlMjBzcG90bGlnaHR8ZW58MXx8fHwxNzc1Mzk2OTQxfDA&ixlib=rb-4.1.0&q=80&w=1080",
      "https://images.unsplash.com/photo-1765560008448-612e4b17877f?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxjZWxlYnJpdHklMjByZWQlMjBjYXJwZXQlMjBldmVudHxlbnwxfHx8fDE3NzUzOTY5NDJ8MA&ixlib=rb-4.1.0&q=80&w=1080",
      "https://images.unsplash.com/photo-1716187249622-4bd9ae36a24c?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxleGNsdXNpdmUlMjB2aXAlMjBiYWNrc3RhZ2V8ZW58MXx8fHwxNzc1Mzk2OTQyfDA&ixlib=rb-4.1.0&q=80&w=1080",
      "https://images.unsplash.com/photo-1741829186423-43f6fa5ac781?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxtZWV0JTIwYW5kJTIwZ3JlZXQlMjBmYW5zfGVufDF8fHx8MTc3NTM5Njk0Mnww&ixlib=rb-4.1.0&q=80&w=1080"
    ]
  }
};

export interface CelebData {
  name: string;
  management: string;
  tagline: string;
  heroText: string;
  stats: {
    meetGreets: number;
    privateTime: number;
    ticketsSold: number;
    fanCards: number;
  };
  bio: string;
  interests: string[];
  heroImage: string;
  photos: string[];
}

export const services = [
  {
    id: "fan-card",
    name: "Official Fan Card",
    description: "Get your exclusive verified fan card with special perks"
  },
  {
    id: "meet-greet",
    name: "Meet & Greet",
    description: "Personal meet and greet session with your favorite celebrity"
  },
  {
    id: "tickets",
    name: "Concert Tickets",
    description: "Premium tickets to upcoming shows and events"
  },
  {
    id: "premium-seats",
    name: "Premium VIP Seats",
    description: "Front row and VIP seating arrangements"
  },
  {
    id: "after-event",
    name: "After Event Meet-up",
    description: "Exclusive backstage access after the show"
  },
  {
    id: "photo-time",
    name: "Photo Session",
    description: "Professional photo opportunity with the celebrity"
  },
  {
    id: "private-time",
    name: "Private Time Together",
    description: "One-on-one exclusive time with the celebrity"
  }
];
