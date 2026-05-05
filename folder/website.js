import React, { useState, useEffect } from 'react';
import { ChevronDown, Menu, X, ArrowRight, Globe, MessageSquare, Share2 } from 'lucide-react';

const ModernWebsite = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isDark, setIsDark] = useState(true);
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [scrollPosition, setScrollPosition] = useState(0);

  useEffect(() => {
    const handleScroll = () => {
      setScrollPosition(window.scrollY);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <div className={`min-h-screen ${isDark ? 'bg-gray-900 text-white' : 'bg-white text-gray-900'}`}>
      {/* Enhanced Header with Blur Effect */}
      <header className={`fixed w-full transition-all duration-300 ${
        scrollPosition > 50 ? 'bg-opacity-80 backdrop-blur-lg' : ''
      } ${isDark ? 'bg-gray-900' : 'bg-white'} z-50`}>
        <div className="container mx-auto px-4">
          <div className="flex items-center justify-between h-16">
            {/* Logo */}
            <div className="flex items-center space-x-2">
              <div className="w-8 h-8 bg-blue-500 rounded-lg animate-pulse"></div>
              <span className="text-xl font-bold bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">
                Projects.AI
              </span>
            </div>

            {/* Desktop Navigation */}
            <nav className="hidden md:flex items-center space-x-8">
              <NavLink href="#" label="Home" />
              <NavLink href="#" label="Features" />
              <NavLink href="#" label="Pricing" />
              <NavLink href="#" label="About" />
            </nav>

            {/* Actions */}
            <div className="flex items-center space-x-4">
              <button 
                onClick={() => setIsDark(!isDark)}
                className="p-2 rounded-full hover:bg-gray-800 transition-colors"
              >
                {isDark ? '🌞' : '🌙'}
              </button>
              
              <button 
                onClick={() => setIsModalOpen(true)}
                className="hidden md:block px-4 py-2 bg-blue-500 hover:bg-blue-600 rounded-lg transition-colors"
              >
                Get Started
              </button>

              {/* Mobile Menu Button */}
              <button 
                onClick={() => setIsMenuOpen(!isMenuOpen)}
                className="md:hidden p-2"
              >
                {isMenuOpen ? <X /> : <Menu />}
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Mobile Menu */}
      {isMenuOpen && (
        <div className="fixed inset-0 z-40 bg-gray-900 bg-opacity-50 backdrop-blur-sm">
          <div className={`fixed inset-y-0 right-0 w-64 ${isDark ? 'bg-gray-900' : 'bg-white'} p-6 transform transition-transform duration-300 ease-in-out`}>
            <div className="flex flex-col space-y-4">
              <NavLink href="#" label="Home" mobile />
              <NavLink href="#" label="Features" mobile />
              <NavLink href="#" label="Pricing" mobile />
              <NavLink href="#" label="About" mobile />
            </div>
          </div>
        </div>
      )}

      {/* Hero Section */}
      <section className="pt-32 pb-20 px-4">
        <div className="container mx-auto text-center">
          <h1 className="text-5xl md:text-6xl font-bold mb-6 bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">
            Welcome to AI ChatBot
          </h1>
          <p className="text-xl mb-8 text-gray-400 max-w-2xl mx-auto">
            Experience the future of project management with our AI-powered assistant.
            Get instant guidance, smart suggestions, and seamless collaboration.
          </p>
          <div className="flex flex-col md:flex-row justify-center gap-4">
            <button 
              onClick={() => setIsModalOpen(true)}
              className="px-8 py-3 bg-blue-500 hover:bg-blue-600 rounded-lg transition-all hover:scale-105"
            >
              Get Started Free
            </button>
            <button className="px-8 py-3 border border-blue-500 rounded-lg hover:bg-blue-500/10 transition-all">
              Learn More
            </button>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 px-4">
        <div className="container mx-auto">
          <div className="grid md:grid-cols-3 gap-8">
            <FeatureCard 
              title="Smart AI Assistant"
              description="Get intelligent suggestions and automated workflows powered by advanced AI"
              icon="🤖"
            />
            <FeatureCard 
              title="Real-time Collaboration"
              description="Work together seamlessly with your team in real-time"
              icon="👥"
            />
            <FeatureCard 
              title="Advanced Analytics"
              description="Track progress and gain insights with detailed analytics"
              icon="📊"
            />
          </div>
        </div>
      </section>

      {/* Pricing Section */}
      <section className="py-20 px-4 bg-gray-800/50">
        <div className="container mx-auto">
          <h2 className="text-3xl font-bold text-center mb-12">Choose Your Plan</h2>
          <div className="grid md:grid-cols-2 gap-8 max-w-4xl mx-auto">
            <PricingCard 
              title="Freemium"
              price="$0"
              features={[
                'Basic AI assistance',
                'Up to 3 projects',
                'Community support'
              ]}
            />
            <PricingCard 
              title="Premium"
              price="$19"
              features={[
                'Advanced AI features',
                'Unlimited projects',
                'Priority support',
                'Custom workflows'
              ]}
              highlighted
            />
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-12 px-4 bg-gray-800/30">
        <div className="container mx-auto">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <div className="text-gray-400 mb-4 md:mb-0">
              © 2024 Projects.AI. All rights reserved.
            </div>
            <div className="flex space-x-6">
              <SocialIcon Icon={Globe} />
              <SocialIcon Icon={MessageSquare} />
              <SocialIcon Icon={Share2} />
            </div>
          </div>
        </div>
      </footer>

      {/* Modal */}
      {isModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50 backdrop-blur-sm">
          <div className="bg-gray-800 p-8 rounded-lg w-full max-w-md">
            <div className="flex justify-between items-center mb-6">
              <h3 className="text-xl font-bold">Get Started</h3>
              <button onClick={() => setIsModalOpen(false)}>
                <X className="h-6 w-6" />
              </button>
            </div>
            <form className="space-y-4">
              <input
                type="email"
                placeholder="Email"
                className="w-full p-3 rounded-lg bg-gray-700"
              />
              <input
                type="password"
                placeholder="Password"
                className="w-full p-3 rounded-lg bg-gray-700"
              />
              <button
                type="submit"
                className="w-full py-3 bg-blue-500 hover:bg-blue-600 rounded-lg transition-colors"
              >
                Sign Up
              </button>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

const NavLink = ({ href, label, mobile }) => (
  <a
    href={href}
    className={`${
      mobile ? 'block' : 'inline-block'
    } hover:text-blue-400 transition-colors`}
  >
    {label}
  </a>
);

const FeatureCard = ({ title, description, icon }) => (
  <div className="p-6 rounded-lg bg-gray-800/30 hover:bg-gray-800/50 transition-all hover:scale-105">
    <div className="text-4xl mb-4">{icon}</div>
    <h3 className="text-xl font-bold mb-2">{title}</h3>
    <p className="text-gray-400">{description}</p>
  </div>
);

const PricingCard = ({ title, price, features, highlighted }) => (
  <div className={`p-6 rounded-lg ${
    highlighted ? 'bg-blue-500/20 border border-blue-500' : 'bg-gray-800/30'
  }`}>
    <h3 className="text-xl font-bold mb-2">{title}</h3>
    <div className="text-3xl font-bold mb-4">{price}<span className="text-sm font-normal">/month</span></div>
    <ul className="space-y-2">
      {features.map((feature, index) => (
        <li key={index} className="flex items-center space-x-2">
          <ArrowRight className="h-4 w-4" />
          <span>{feature}</span>
        </li>
      ))}
    </ul>
    <button className={`w-full py-2 mt-6 rounded-lg transition-colors ${
      highlighted ? 'bg-blue-500 hover:bg-blue-600' : 'bg-gray-700 hover:bg-gray-600'
    }`}>
      Get Started
    </button>
  </div>
);

const SocialIcon = ({ Icon }) => (
  <a href="#" className="hover:text-blue-400 transition-colors">
    <Icon className="h-6 w-6" />
  </a>
);

export default ModernWebsite;