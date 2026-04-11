import { useState, useEffect } from "react";
import { motion } from "motion/react";
import { Lock, Mail, Send, Check, X, Eye, Trash2, Search, Filter } from "lucide-react";
import { Button } from "../components/ui/button";
import { Input } from "../components/ui/input";
import { Textarea } from "../components/ui/textarea";
import { Card } from "../components/ui/card";
import { Badge } from "../components/ui/badge";
import { Checkbox } from "../components/ui/checkbox";

interface BookingEntry {
  id: string;
  name: string;
  email: string;
  phone: string;
  country: string;
  address: string;
  selectedServices: string[];
  message: string;
  occupation: string;
  age: string;
  submittedAt: string;
  emailSent: boolean;
}

export function AdminDashboard() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [password, setPassword] = useState("");
  const [entries, setEntries] = useState<BookingEntry[]>([]);
  const [selectedEntries, setSelectedEntries] = useState<string[]>([]);
  const [showEmailComposer, setShowEmailComposer] = useState(false);
  const [emailSubject, setEmailSubject] = useState("");
  const [emailBody, setEmailBody] = useState("");
  const [searchQuery, setSearchQuery] = useState("");
  const [filterStatus, setFilterStatus] = useState<"all" | "sent" | "unsent">("all");

  // Load mock data
  useEffect(() => {
    if (isAuthenticated) {
      // Mock booking entries
      const mockEntries: BookingEntry[] = [
        {
          id: "1",
          name: "Sarah Johnson",
          email: "sarah.johnson@email.com",
          phone: "+1234567890",
          country: "United States",
          address: "New York, NY",
          selectedServices: ["meet-greet", "photo-time"],
          message: "Huge fan! Would love to meet you!",
          occupation: "Teacher",
          age: "28",
          submittedAt: new Date().toISOString(),
          emailSent: false
        },
        {
          id: "2",
          name: "Michael Chen",
          email: "mchen@email.com",
          phone: "+9876543210",
          country: "Canada",
          address: "Toronto, ON",
          selectedServices: ["all"],
          message: "This would be a dream come true!",
          occupation: "Software Engineer",
          age: "32",
          submittedAt: new Date(Date.now() - 86400000).toISOString(),
          emailSent: true
        },
        {
          id: "3",
          name: "Emma Williams",
          email: "emma.w@email.com",
          phone: "+1122334455",
          country: "United Kingdom",
          address: "London",
          selectedServices: ["tickets", "premium-seats"],
          message: "",
          occupation: "Marketing Manager",
          age: "25",
          submittedAt: new Date(Date.now() - 172800000).toISOString(),
          emailSent: false
        }
      ];
      setEntries(mockEntries);
    }
  }, [isAuthenticated]);

  const handleLogin = (e: React.FormEvent) => {
    e.preventDefault();
    // Simple password check (in real app, use proper authentication)
    if (password === "admin123") {
      setIsAuthenticated(true);
    } else {
      alert("Incorrect password");
    }
  };

  const handleSelectEntry = (id: string) => {
    setSelectedEntries(prev =>
      prev.includes(id) ? prev.filter(e => e !== id) : [...prev, id]
    );
  };

  const handleSelectAll = () => {
    if (selectedEntries.length === filteredEntries.length) {
      setSelectedEntries([]);
    } else {
      setSelectedEntries(filteredEntries.map(e => e.id));
    }
  };

  const handleSendEmail = (entryIds: string[]) => {
    // Mark as sent
    setEntries(prev =>
      prev.map(entry =>
        entryIds.includes(entry.id) ? { ...entry, emailSent: true } : entry
      )
    );
    alert(`Email sent to ${entryIds.length} recipient(s)`);
    setSelectedEntries([]);
    setShowEmailComposer(false);
    setEmailSubject("");
    setEmailBody("");
  };

  const handleDeleteEntry = (id: string) => {
    if (confirm("Are you sure you want to delete this entry?")) {
      setEntries(prev => prev.filter(e => e.id !== id));
    }
  };

  const filteredEntries = entries.filter(entry => {
    const matchesSearch =
      entry.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      entry.email.toLowerCase().includes(searchQuery.toLowerCase()) ||
      entry.country.toLowerCase().includes(searchQuery.toLowerCase());

    const matchesFilter =
      filterStatus === "all" ||
      (filterStatus === "sent" && entry.emailSent) ||
      (filterStatus === "unsent" && !entry.emailSent);

    return matchesSearch && matchesFilter;
  });

  if (!isAuthenticated) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-900 via-blue-900 to-black flex items-center justify-center p-4">
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          className="bg-white/10 backdrop-blur-xl border border-white/20 rounded-3xl p-12 shadow-2xl max-w-md w-full"
        >
          <div className="text-center mb-8">
            <div className="inline-block bg-purple-600 p-4 rounded-full mb-4">
              <Lock className="w-8 h-8 text-white" />
            </div>
            <h1 className="text-3xl text-white mb-2">Admin Dashboard</h1>
            <p className="text-white/70">Enter password to access</p>
          </div>

          <form onSubmit={handleLogin} className="space-y-4">
            <Input
              type="password"
              placeholder="Enter admin password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="bg-white/10 border-white/20 text-white placeholder:text-white/50"
            />
            <Button type="submit" className="w-full bg-gradient-to-r from-purple-600 to-pink-600">
              Login
            </Button>
          </form>

          <p className="text-center text-white/50 text-sm mt-4">
            Demo password: admin123
          </p>
        </motion.div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-black via-purple-950/20 to-black text-white">
      {/* Header */}
      <header className="border-b border-white/10 bg-black/80 backdrop-blur-lg sticky top-0 z-40">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <h1 className="text-2xl">Admin Dashboard</h1>
            <Button
              variant="outline"
              onClick={() => setIsAuthenticated(false)}
              className="border-white/20 text-white hover:bg-white/10"
            >
              Logout
            </Button>
          </div>
        </div>
      </header>

      <div className="container mx-auto px-4 py-8">
        {/* Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
          <Card className="bg-white/5 border-white/10 p-6">
            <div className="text-3xl text-purple-400 mb-2">{entries.length}</div>
            <div className="text-white/70">Total Entries</div>
          </Card>
          <Card className="bg-white/5 border-white/10 p-6">
            <div className="text-3xl text-green-400 mb-2">
              {entries.filter(e => e.emailSent).length}
            </div>
            <div className="text-white/70">Emails Sent</div>
          </Card>
          <Card className="bg-white/5 border-white/10 p-6">
            <div className="text-3xl text-yellow-400 mb-2">
              {entries.filter(e => !e.emailSent).length}
            </div>
            <div className="text-white/70">Pending</div>
          </Card>
          <Card className="bg-white/5 border-white/10 p-6">
            <div className="text-3xl text-blue-400 mb-2">{selectedEntries.length}</div>
            <div className="text-white/70">Selected</div>
          </Card>
        </div>

        {/* Actions */}
        <div className="flex flex-wrap gap-4 mb-6">
          <Button
            onClick={() => setShowEmailComposer(!showEmailComposer)}
            disabled={selectedEntries.length === 0}
            className="bg-purple-600 hover:bg-purple-700"
          >
            <Mail className="w-4 h-4 mr-2" />
            Compose Email ({selectedEntries.length})
          </Button>
          {selectedEntries.length > 0 && (
            <Button
              onClick={() => setSelectedEntries([])}
              variant="outline"
              className="border-white/20 text-white hover:bg-white/10"
            >
              Clear Selection
            </Button>
          )}
        </div>

        {/* Email Composer */}
        {showEmailComposer && selectedEntries.length > 0 && (
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-white/5 border border-white/10 rounded-2xl p-6 mb-6"
          >
            <h2 className="text-xl mb-4">Compose Email</h2>
            <div className="space-y-4">
              <div>
                <label className="text-sm text-white/70 mb-2 block">To:</label>
                <div className="flex flex-wrap gap-2">
                  {entries
                    .filter(e => selectedEntries.includes(e.id))
                    .map(e => (
                      <Badge key={e.id} variant="outline" className="border-purple-400/30 text-purple-300">
                        {e.email}
                      </Badge>
                    ))}
                </div>
              </div>

              <div>
                <label className="text-sm text-white/70 mb-2 block">Subject:</label>
                <Input
                  value={emailSubject}
                  onChange={(e) => setEmailSubject(e.target.value)}
                  placeholder="Email subject"
                  className="bg-white/10 border-white/20 text-white placeholder:text-white/50"
                />
              </div>

              <div>
                <label className="text-sm text-white/70 mb-2 block">Message:</label>
                <Textarea
                  value={emailBody}
                  onChange={(e) => setEmailBody(e.target.value)}
                  placeholder="Email body"
                  className="bg-white/10 border-white/20 text-white placeholder:text-white/50 min-h-[200px]"
                />
              </div>

              <div className="flex gap-4">
                <Button
                  onClick={() => handleSendEmail(selectedEntries)}
                  className="bg-green-600 hover:bg-green-700"
                >
                  <Send className="w-4 h-4 mr-2" />
                  Send Email
                </Button>
                <Button
                  onClick={() => setShowEmailComposer(false)}
                  variant="outline"
                  className="border-white/20 text-white hover:bg-white/10"
                >
                  Cancel
                </Button>
              </div>
            </div>
          </motion.div>
        )}

        {/* Search & Filter */}
        <div className="flex flex-wrap gap-4 mb-6">
          <div className="flex-1 min-w-[200px]">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-white/50" />
              <Input
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Search entries..."
                className="bg-white/10 border-white/20 text-white placeholder:text-white/50 pl-10"
              />
            </div>
          </div>
          <div className="flex gap-2">
            <Button
              onClick={() => setFilterStatus("all")}
              variant={filterStatus === "all" ? "default" : "outline"}
              className={filterStatus === "all" ? "bg-purple-600" : "border-white/20 text-white hover:bg-white/10"}
            >
              All
            </Button>
            <Button
              onClick={() => setFilterStatus("sent")}
              variant={filterStatus === "sent" ? "default" : "outline"}
              className={filterStatus === "sent" ? "bg-purple-600" : "border-white/20 text-white hover:bg-white/10"}
            >
              Sent
            </Button>
            <Button
              onClick={() => setFilterStatus("unsent")}
              variant={filterStatus === "unsent" ? "default" : "outline"}
              className={filterStatus === "unsent" ? "bg-purple-600" : "border-white/20 text-white hover:bg-white/10"}
            >
              Pending
            </Button>
          </div>
        </div>

        {/* Entries Table */}
        <div className="bg-white/5 border border-white/10 rounded-2xl overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-white/5 border-b border-white/10">
                <tr>
                  <th className="p-4 text-left">
                    <Checkbox
                      checked={selectedEntries.length === filteredEntries.length && filteredEntries.length > 0}
                      onCheckedChange={handleSelectAll}
                    />
                  </th>
                  <th className="p-4 text-left text-white/70">Name</th>
                  <th className="p-4 text-left text-white/70">Email</th>
                  <th className="p-4 text-left text-white/70">Phone</th>
                  <th className="p-4 text-left text-white/70">Country</th>
                  <th className="p-4 text-left text-white/70">Services</th>
                  <th className="p-4 text-left text-white/70">Date</th>
                  <th className="p-4 text-left text-white/70">Status</th>
                  <th className="p-4 text-left text-white/70">Actions</th>
                </tr>
              </thead>
              <tbody>
                {filteredEntries.map((entry) => (
                  <tr key={entry.id} className="border-b border-white/5 hover:bg-white/5">
                    <td className="p-4">
                      <Checkbox
                        checked={selectedEntries.includes(entry.id)}
                        onCheckedChange={() => handleSelectEntry(entry.id)}
                      />
                    </td>
                    <td className="p-4 text-white">{entry.name}</td>
                    <td className="p-4">
                      <a href={`mailto:${entry.email}`} className="text-purple-400 hover:underline">
                        {entry.email}
                      </a>
                    </td>
                    <td className="p-4 text-white/70">{entry.phone}</td>
                    <td className="p-4 text-white/70">{entry.country}</td>
                    <td className="p-4">
                      <div className="flex flex-wrap gap-1">
                        {entry.selectedServices.slice(0, 2).map((service, i) => (
                          <Badge key={i} variant="outline" className="text-xs border-purple-400/30 text-purple-300">
                            {service}
                          </Badge>
                        ))}
                        {entry.selectedServices.length > 2 && (
                          <Badge variant="outline" className="text-xs border-purple-400/30 text-purple-300">
                            +{entry.selectedServices.length - 2}
                          </Badge>
                        )}
                      </div>
                    </td>
                    <td className="p-4 text-white/70">
                      {new Date(entry.submittedAt).toLocaleDateString()}
                    </td>
                    <td className="p-4">
                      {entry.emailSent ? (
                        <Badge className="bg-green-600/20 text-green-400 border-green-400/30">
                          <Check className="w-3 h-3 mr-1" />
                          Sent
                        </Badge>
                      ) : (
                        <Badge className="bg-yellow-600/20 text-yellow-400 border-yellow-400/30">
                          Pending
                        </Badge>
                      )}
                    </td>
                    <td className="p-4">
                      <div className="flex gap-2">
                        <Button
                          size="sm"
                          variant="outline"
                          onClick={() => {
                            setSelectedEntries([entry.id]);
                            setShowEmailComposer(true);
                          }}
                          className="border-white/20 text-white hover:bg-white/10"
                        >
                          <Mail className="w-4 h-4" />
                        </Button>
                        <Button
                          size="sm"
                          variant="outline"
                          onClick={() => handleDeleteEntry(entry.id)}
                          className="border-red-400/20 text-red-400 hover:bg-red-400/10"
                        >
                          <Trash2 className="w-4 h-4" />
                        </Button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {filteredEntries.length === 0 && (
            <div className="p-12 text-center text-white/50">
              No entries found
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
