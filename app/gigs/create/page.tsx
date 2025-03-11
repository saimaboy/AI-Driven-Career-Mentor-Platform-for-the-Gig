"use client"

import { Badge } from "@/components/ui/badge"

import type React from "react"

import { useState } from "react"
import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Checkbox } from "@/components/ui/checkbox"
import { Switch } from "@/components/ui/switch"
import {
  AlertCircle,
  ArrowLeft,
  Clock,
  DollarSign,
  FileText,
  Globe,
  Image,
  Laptop,
  Loader2,
  Plus,
  Star,
  UploadCloud,
} from "lucide-react"
import { Separator } from "@/components/ui/separator"
import { toast } from "@/hooks/use-toast"

export default function CreateGigPage() {
  const [isLoading, setIsLoading] = useState(false)
  const [activeTab, setActiveTab] = useState("overview")
  const [formData, setFormData] = useState({
    title: "",
    category: "",
    subcategory: "",
    description: "",
    tags: [],
    price: {
      basic: "50",
      standard: "100",
      premium: "200",
    },
    deliveryTime: {
      basic: "3",
      standard: "5",
      premium: "7",
    },
    revisions: {
      basic: "1",
      standard: "3",
      premium: "unlimited",
    },
    featuredImage: null,
    gallery: [],
    requirements: "",
    faq: [],
    platforms: ["fiverr"],
    searchTags: "",
    sourceFiles: false,
    commercial: false,
    rush: false,
  })

  const [currentFaq, setCurrentFaq] = useState({ question: "", answer: "" })

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target
    setFormData((prev) => ({ ...prev, [name]: value }))
  }

  const handleSelectChange = (name: string, value: string) => {
    setFormData((prev) => ({ ...prev, [name]: value }))
  }

  const handlePriceChange = (tier: string, value: string) => {
    setFormData((prev) => ({
      ...prev,
      price: {
        ...prev.price,
        [tier]: value,
      },
    }))
  }

  const handleDeliveryChange = (tier: string, value: string) => {
    setFormData((prev) => ({
      ...prev,
      deliveryTime: {
        ...prev.deliveryTime,
        [tier]: value,
      },
    }))
  }

  const handleAddFaq = () => {
    if (currentFaq.question.trim() && currentFaq.answer.trim()) {
      setFormData((prev) => ({
        ...prev,
        faq: [...prev.faq, { ...currentFaq }],
      }))
      setCurrentFaq({ question: "", answer: "" })
    }
  }

  const handleFaqChange = (field: string, value: string) => {
    setCurrentFaq((prev) => ({
      ...prev,
      [field]: value,
    }))
  }

  const handleRemoveFaq = (index: number) => {
    setFormData((prev) => ({
      ...prev,
      faq: prev.faq.filter((_, i) => i !== index),
    }))
  }

  const handleTogglePlatform = (platform: string) => {
    setFormData((prev) => {
      const platforms = [...prev.platforms]
      if (platforms.includes(platform)) {
        return { ...prev, platforms: platforms.filter((p) => p !== platform) }
      } else {
        return { ...prev, platforms: [...platforms, platform] }
      }
    })
  }

  const handleSwitchChange = (name: string, checked: boolean) => {
    setFormData((prev) => ({ ...prev, [name]: checked }))
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)

    try {
      // Simulate API call
      await new Promise((resolve) => setTimeout(resolve, 1500))
      console.log("Gig data:", formData)

      // Show success toast
      toast({
        title: "Gig created successfully",
        description: "Your gig has been created and is ready to publish to selected platforms.",
      })

      // Redirect to gigs page on success
      window.location.href = "/gigs"
    } catch (error) {
      console.error("Error creating gig:", error)

      // Show error toast
      toast({
        title: "Error creating gig",
        description: "There was a problem creating your gig. Please try again.",
        variant: "destructive",
      })
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="container max-w-6xl py-10">
      <div className="flex flex-col space-y-6">
        <div className="flex items-center gap-2">
          <Button variant="ghost" size="sm" asChild>
            <Link href="/dashboard">
              <ArrowLeft className="h-4 w-4 mr-1" />
              Back to Dashboard
            </Link>
          </Button>
        </div>

        <div className="flex flex-col space-y-2">
          <h1 className="text-3xl font-bold">Create New Gig</h1>
          <p className="text-muted-foreground">
            Create a compelling gig that showcases your skills and attracts the right clients
          </p>
        </div>

        <Tabs defaultValue="overview" value={activeTab} onValueChange={setActiveTab} className="w-full">
          <TabsList className="grid w-full grid-cols-4">
            <TabsTrigger value="overview">Overview</TabsTrigger>
            <TabsTrigger value="pricing">Pricing & Packages</TabsTrigger>
            <TabsTrigger value="description">Description & FAQ</TabsTrigger>
            <TabsTrigger value="publish">Gallery & Publish</TabsTrigger>
          </TabsList>

          <form onSubmit={handleSubmit}>
            <TabsContent value="overview" className="space-y-6 mt-6">
              <Card>
                <CardHeader>
                  <CardTitle>Gig Overview</CardTitle>
                  <CardDescription>Provide the basic information about your service</CardDescription>
                </CardHeader>
                <CardContent className="space-y-6">
                  <div className="space-y-2">
                    <Label htmlFor="title">Gig Title</Label>
                    <Input
                      id="title"
                      name="title"
                      placeholder="I will create a professional website with React"
                      required
                      maxLength={80}
                      value={formData.title}
                      onChange={handleChange}
                    />
                    <p className="text-xs text-muted-foreground">
                      Clearly describe your service in 80 characters or less
                    </p>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div className="space-y-2">
                      <Label htmlFor="category">Category</Label>
                      <Select
                        value={formData.category}
                        onValueChange={(value) => handleSelectChange("category", value)}
                      >
                        <SelectTrigger>
                          <SelectValue placeholder="Select a category" />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="web-development">Web Development</SelectItem>
                          <SelectItem value="mobile-development">Mobile Development</SelectItem>
                          <SelectItem value="design">Design & Creative</SelectItem>
                          <SelectItem value="writing">Writing & Translation</SelectItem>
                          <SelectItem value="video">Video & Animation</SelectItem>
                          <SelectItem value="music">Music & Audio</SelectItem>
                          <SelectItem value="marketing">Digital Marketing</SelectItem>
                          <SelectItem value="business">Business</SelectItem>
                        </SelectContent>
                      </Select>
                    </div>

                    <div className="space-y-2">
                      <Label htmlFor="subcategory">Subcategory</Label>
                      <Select
                        value={formData.subcategory}
                        onValueChange={(value) => handleSelectChange("subcategory", value)}
                        disabled={!formData.category}
                      >
                        <SelectTrigger>
                          <SelectValue placeholder="Select a subcategory" />
                        </SelectTrigger>
                        <SelectContent>
                          {formData.category === "web-development" && (
                            <>
                              <SelectItem value="website-development">Website Development</SelectItem>
                              <SelectItem value="ecommerce">E-commerce Development</SelectItem>
                              <SelectItem value="landing-page">Landing Page</SelectItem>
                              <SelectItem value="web-app">Web Application</SelectItem>
                              <SelectItem value="api">API Development</SelectItem>
                            </>
                          )}
                          {formData.category === "design" && (
                            <>
                              <SelectItem value="ui-ux">UI/UX Design</SelectItem>
                              <SelectItem value="graphic-design">Graphic Design</SelectItem>
                              <SelectItem value="logo-design">Logo Design</SelectItem>
                              <SelectItem value="branding">Brand Identity</SelectItem>
                            </>
                          )}
                          {/* Add more subcategories based on the selected category */}
                        </SelectContent>
                      </Select>
                    </div>
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="searchTags">Search Tags</Label>
                    <Input
                      id="searchTags"
                      name="searchTags"
                      placeholder="web design, react, responsive, ecommerce (comma separated)"
                      value={formData.searchTags}
                      onChange={handleChange}
                    />
                    <p className="text-xs text-muted-foreground">
                      Add keywords that potential buyers would use to find your service
                    </p>
                  </div>
                </CardContent>
                <CardFooter className="flex justify-between">
                  <div></div>
                  <Button type="button" onClick={() => setActiveTab("pricing")}>
                    Continue to Pricing
                  </Button>
                </CardFooter>
              </Card>
            </TabsContent>

            <TabsContent value="pricing" className="space-y-6 mt-6">
              <Card>
                <CardHeader>
                  <CardTitle>Pricing & Packages</CardTitle>
                  <CardDescription>Define your packages, pricing, and delivery options</CardDescription>
                </CardHeader>
                <CardContent className="space-y-6">
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div className="col-span-1 md:col-span-3">
                      <h3 className="text-lg font-medium mb-4">Package Tiers</h3>
                      <p className="text-sm text-muted-foreground mb-4">
                        Create up to three package tiers to give clients options at different price points.
                      </p>
                    </div>

                    <Card className="border-2">
                      <CardHeader className="pb-2">
                        <CardTitle className="text-md flex items-center">Basic</CardTitle>
                        <CardDescription>Entry level service</CardDescription>
                      </CardHeader>
                      <CardContent className="space-y-4">
                        <div className="space-y-2">
                          <Label htmlFor="basicPrice">Price ($)</Label>
                          <div className="relative">
                            <DollarSign className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
                            <Input
                              id="basicPrice"
                              type="number"
                              className="pl-8"
                              value={formData.price.basic}
                              onChange={(e) => handlePriceChange("basic", e.target.value)}
                            />
                          </div>
                        </div>
                        <div className="space-y-2">
                          <Label htmlFor="basicDelivery">Delivery Time (days)</Label>
                          <div className="relative">
                            <Clock className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
                            <Input
                              id="basicDelivery"
                              type="number"
                              className="pl-8"
                              value={formData.deliveryTime.basic}
                              onChange={(e) => handleDeliveryChange("basic", e.target.value)}
                            />
                          </div>
                        </div>
                        <div className="space-y-2">
                          <Label htmlFor="basicRevisions">Number of Revisions</Label>
                          <Select
                            value={formData.revisions.basic}
                            onValueChange={(value) => {
                              setFormData((prev) => ({
                                ...prev,
                                revisions: {
                                  ...prev.revisions,
                                  basic: value,
                                },
                              }))
                            }}
                          >
                            <SelectTrigger id="basicRevisions">
                              <SelectValue placeholder="Select revisions" />
                            </SelectTrigger>
                            <SelectContent>
                              <SelectItem value="1">1 revision</SelectItem>
                              <SelectItem value="2">2 revisions</SelectItem>
                              <SelectItem value="3">3 revisions</SelectItem>
                              <SelectItem value="5">5 revisions</SelectItem>
                              <SelectItem value="unlimited">Unlimited</SelectItem>
                            </SelectContent>
                          </Select>
                        </div>
                      </CardContent>
                    </Card>

                    <Card className="border-2 border-primary">
                      <CardHeader className="pb-2">
                        <div className="flex justify-between items-center">
                          <CardTitle className="text-md">Standard</CardTitle>
                          <Badge>Recommended</Badge>
                        </div>
                        <CardDescription>Most popular option</CardDescription>
                      </CardHeader>
                      <CardContent className="space-y-4">
                        <div className="space-y-2">
                          <Label htmlFor="standardPrice">Price ($)</Label>
                          <div className="relative">
                            <DollarSign className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
                            <Input
                              id="standardPrice"
                              type="number"
                              className="pl-8"
                              value={formData.price.standard}
                              onChange={(e) => handlePriceChange("standard", e.target.value)}
                            />
                          </div>
                        </div>
                        <div className="space-y-2">
                          <Label htmlFor="standardDelivery">Delivery Time (days)</Label>
                          <div className="relative">
                            <Clock className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
                            <Input
                              id="standardDelivery"
                              type="number"
                              className="pl-8"
                              value={formData.deliveryTime.standard}
                              onChange={(e) => handleDeliveryChange("standard", e.target.value)}
                            />
                          </div>
                        </div>
                        <div className="space-y-2">
                          <Label htmlFor="standardRevisions">Number of Revisions</Label>
                          <Select
                            value={formData.revisions.standard}
                            onValueChange={(value) => {
                              setFormData((prev) => ({
                                ...prev,
                                revisions: {
                                  ...prev.revisions,
                                  standard: value,
                                },
                              }))
                            }}
                          >
                            <SelectTrigger id="standardRevisions">
                              <SelectValue placeholder="Select revisions" />
                            </SelectTrigger>
                            <SelectContent>
                              <SelectItem value="1">1 revision</SelectItem>
                              <SelectItem value="2">2 revisions</SelectItem>
                              <SelectItem value="3">3 revisions</SelectItem>
                              <SelectItem value="5">5 revisions</SelectItem>
                              <SelectItem value="unlimited">Unlimited</SelectItem>
                            </SelectContent>
                          </Select>
                        </div>
                      </CardContent>
                    </Card>

                    <Card className="border-2">
                      <CardHeader className="pb-2">
                        <CardTitle className="text-md">Premium</CardTitle>
                        <CardDescription>Complete service package</CardDescription>
                      </CardHeader>
                      <CardContent className="space-y-4">
                        <div className="space-y-2">
                          <Label htmlFor="premiumPrice">Price ($)</Label>
                          <div className="relative">
                            <DollarSign className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
                            <Input
                              id="premiumPrice"
                              type="number"
                              className="pl-8"
                              value={formData.price.premium}
                              onChange={(e) => handlePriceChange("premium", e.target.value)}
                            />
                          </div>
                        </div>
                        <div className="space-y-2">
                          <Label htmlFor="premiumDelivery">Delivery Time (days)</Label>
                          <div className="relative">
                            <Clock className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
                            <Input
                              id="premiumDelivery"
                              type="number"
                              className="pl-8"
                              value={formData.deliveryTime.premium}
                              onChange={(e) => handleDeliveryChange("premium", e.target.value)}
                            />
                          </div>
                        </div>
                        <div className="space-y-2">
                          <Label htmlFor="premiumRevisions">Number of Revisions</Label>
                          <Select
                            value={formData.revisions.premium}
                            onValueChange={(value) => {
                              setFormData((prev) => ({
                                ...prev,
                                revisions: {
                                  ...prev.revisions,
                                  premium: value,
                                },
                              }))
                            }}
                          >
                            <SelectTrigger id="premiumRevisions">
                              <SelectValue placeholder="Select revisions" />
                            </SelectTrigger>
                            <SelectContent>
                              <SelectItem value="1">1 revision</SelectItem>
                              <SelectItem value="2">2 revisions</SelectItem>
                              <SelectItem value="3">3 revisions</SelectItem>
                              <SelectItem value="5">5 revisions</SelectItem>
                              <SelectItem value="unlimited">Unlimited</SelectItem>
                            </SelectContent>
                          </Select>
                        </div>
                      </CardContent>
                    </Card>
                  </div>

                  <Separator />

                  <div className="space-y-4">
                    <h3 className="text-lg font-medium">Additional Options</h3>

                    <div className="flex items-center justify-between">
                      <div className="space-y-0.5">
                        <Label htmlFor="sourceFiles">Source Files</Label>
                        <p className="text-sm text-muted-foreground">Include source files in delivery</p>
                      </div>
                      <Switch
                        id="sourceFiles"
                        checked={formData.sourceFiles}
                        onCheckedChange={(checked) => handleSwitchChange("sourceFiles", checked)}
                      />
                    </div>

                    <div className="flex items-center justify-between">
                      <div className="space-y-0.5">
                        <Label htmlFor="commercial">Commercial Use</Label>
                        <p className="text-sm text-muted-foreground">Allow commercial use of delivered work</p>
                      </div>
                      <Switch
                        id="commercial"
                        checked={formData.commercial}
                        onCheckedChange={(checked) => handleSwitchChange("commercial", checked)}
                      />
                    </div>

                    <div className="flex items-center justify-between">
                      <div className="space-y-0.5">
                        <Label htmlFor="rush">Rush Delivery</Label>
                        <p className="text-sm text-muted-foreground">Offer expedited delivery for an additional fee</p>
                      </div>
                      <Switch
                        id="rush"
                        checked={formData.rush}
                        onCheckedChange={(checked) => handleSwitchChange("rush", checked)}
                      />
                    </div>
                  </div>
                </CardContent>
                <CardFooter className="flex justify-between">
                  <Button type="button" variant="outline" onClick={() => setActiveTab("overview")}>
                    Back to Overview
                  </Button>
                  <Button type="button" onClick={() => setActiveTab("description")}>
                    Continue to Description
                  </Button>
                </CardFooter>
              </Card>
            </TabsContent>

            <TabsContent value="description" className="space-y-6 mt-6">
              <Card>
                <CardHeader>
                  <CardTitle>Description & Requirements</CardTitle>
                  <CardDescription>
                    Provide detailed information about your service and what you need from clients
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-6">
                  <div className="space-y-2">
                    <Label htmlFor="description">Gig Description</Label>
                    <Textarea
                      id="description"
                      name="description"
                      placeholder="Describe your service in detail. Be specific about what you're offering, your process, and what makes your service unique."
                      rows={8}
                      className="resize-y"
                      required
                      value={formData.description}
                      onChange={handleChange}
                    />
                    <div className="flex justify-between items-center">
                      <p className="text-xs text-muted-foreground">
                        Min 120 characters. Use markdown for formatting if needed.
                      </p>
                      <p className="text-xs text-muted-foreground">{formData.description.length} / 1200</p>
                    </div>
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="requirements">Client Requirements</Label>
                    <Textarea
                      id="requirements"
                      name="requirements"
                      placeholder="What information or materials do you need from the client to start working?"
                      rows={4}
                      className="resize-y"
                      value={formData.requirements}
                      onChange={handleChange}
                    />
                    <p className="text-xs text-muted-foreground">
                      Specify any files, information, or access you need from clients
                    </p>
                  </div>

                  <Separator />

                  <div className="space-y-4">
                    <h3 className="text-lg font-medium">Frequently Asked Questions</h3>
                    <p className="text-sm text-muted-foreground">
                      Add FAQs to address common questions clients might have about your service
                    </p>

                    <div className="space-y-4">
                      {formData.faq.map((item, index) => (
                        <Card key={index} className="bg-muted/30">
                          <CardContent className="pt-6">
                            <div className="flex justify-between items-start">
                              <div className="space-y-1">
                                <h4 className="font-medium">{item.question}</h4>
                                <p className="text-sm text-muted-foreground">{item.answer}</p>
                              </div>
                              <Button type="button" variant="ghost" size="sm" onClick={() => handleRemoveFaq(index)}>
                                Remove
                              </Button>
                            </div>
                          </CardContent>
                        </Card>
                      ))}
                    </div>

                    <Card>
                      <CardContent className="pt-6 space-y-4">
                        <div className="space-y-2">
                          <Label htmlFor="faqQuestion">Question</Label>
                          <Input
                            id="faqQuestion"
                            placeholder="E.g., Do you offer website maintenance after completion?"
                            value={currentFaq.question}
                            onChange={(e) => handleFaqChange("question", e.target.value)}
                          />
                        </div>
                        <div className="space-y-2">
                          <Label htmlFor="faqAnswer">Answer</Label>
                          <Textarea
                            id="faqAnswer"
                            placeholder="Provide a clear and concise answer"
                            rows={3}
                            value={currentFaq.answer}
                            onChange={(e) => handleFaqChange("answer", e.target.value)}
                          />
                        </div>
                        <Button
                          type="button"
                          onClick={handleAddFaq}
                          disabled={!currentFaq.question.trim() || !currentFaq.answer.trim()}
                          className="w-full"
                        >
                          <Plus className="h-4 w-4 mr-2" />
                          Add FAQ
                        </Button>
                      </CardContent>
                    </Card>
                  </div>
                </CardContent>
                <CardFooter className="flex justify-between">
                  <Button type="button" variant="outline" onClick={() => setActiveTab("pricing")}>
                    Back to Pricing
                  </Button>
                  <Button type="button" onClick={() => setActiveTab("publish")}>
                    Continue to Gallery & Publish
                  </Button>
                </CardFooter>
              </Card>
            </TabsContent>

            <TabsContent value="publish" className="space-y-6 mt-6">
              <Card>
                <CardHeader>
                  <CardTitle>Gallery & Publish</CardTitle>
                  <CardDescription>
                    Add images and videos to showcase your work and choose where to publish
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-6">
                  <div className="space-y-4">
                    <div className="space-y-2">
                      <Label>Featured Image</Label>
                      <div className="border-2 border-dashed rounded-lg p-6 flex flex-col items-center justify-center">
                        <UploadCloud className="h-10 w-10 text-muted-foreground mb-2" />
                        <p className="text-sm text-muted-foreground mb-1">Drag and drop your featured image here</p>
                        <p className="text-xs text-muted-foreground mb-4">PNG, JPG up to 5MB</p>
                        <Button type="button" variant="outline" size="sm">
                          <Image className="h-4 w-4 mr-2" />
                          Select Image
                        </Button>
                      </div>
                      <p className="text-xs text-muted-foreground">
                        This will be the main image displayed for your gig. Choose a high-quality, professional image.
                      </p>
                    </div>

                    <div className="space-y-2">
                      <Label>Gallery (Optional)</Label>
                      <div className="border-2 border-dashed rounded-lg p-6 flex flex-col items-center justify-center">
                        <UploadCloud className="h-10 w-10 text-muted-foreground mb-2" />
                        <p className="text-sm text-muted-foreground mb-1">Drag and drop additional images here</p>
                        <p className="text-xs text-muted-foreground mb-4">Up to 5 images, 5MB each</p>
                        <Button type="button" variant="outline" size="sm">
                          <Image className="h-4 w-4 mr-2" />
                          Select Images
                        </Button>
                      </div>
                      <p className="text-xs text-muted-foreground">Add more images to showcase examples of your work</p>
                    </div>
                  </div>

                  <Separator />

                  <div className="space-y-4">
                    <h3 className="text-lg font-medium">Publish To Platforms</h3>
                    <p className="text-sm text-muted-foreground">Select where you want to publish your gig</p>

                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                      <Card
                        className={`border-2 cursor-pointer transition-all ${formData.platforms.includes("fiverr") ? "border-primary bg-primary/5" : "border-muted hover:border-primary/50"}`}
                        onClick={() => handleTogglePlatform("fiverr")}
                      >
                        <CardContent className="p-4 flex items-center justify-between">
                          <div className="flex items-center gap-3">
                            <Globe
                              className={`h-5 w-5 ${formData.platforms.includes("fiverr") ? "text-primary" : "text-muted-foreground"}`}
                            />
                            <span className="font-medium">Fiverr</span>
                          </div>
                          <Checkbox checked={formData.platforms.includes("fiverr")} />
                        </CardContent>
                      </Card>

                      <Card
                        className={`border-2 cursor-pointer transition-all ${formData.platforms.includes("upwork") ? "border-primary bg-primary/5" : "border-muted hover:border-primary/50"}`}
                        onClick={() => handleTogglePlatform("upwork")}
                      >
                        <CardContent className="p-4 flex items-center justify-between">
                          <div className="flex items-center gap-3">
                            <Globe
                              className={`h-5 w-5 ${formData.platforms.includes("upwork") ? "text-primary" : "text-muted-foreground"}`}
                            />
                            <span className="font-medium">Upwork</span>
                          </div>
                          <Checkbox checked={formData.platforms.includes("upwork")} />
                        </CardContent>
                      </Card>

                      <Card
                        className={`border-2 cursor-pointer transition-all ${formData.platforms.includes("freelancer") ? "border-primary bg-primary/5" : "border-muted hover:border-primary/50"}`}
                        onClick={() => handleTogglePlatform("freelancer")}
                      >
                        <CardContent className="p-4 flex items-center justify-between">
                          <div className="flex items-center gap-3">
                            <Globe
                              className={`h-5 w-5 ${formData.platforms.includes("freelancer") ? "text-primary" : "text-muted-foreground"}`}
                            />
                            <span className="font-medium">Freelancer.com</span>
                          </div>
                          <Checkbox checked={formData.platforms.includes("freelancer")} />
                        </CardContent>
                      </Card>

                      <Card
                        className={`border-2 cursor-pointer transition-all ${formData.platforms.includes("local") ? "border-primary bg-primary/5" : "border-muted hover:border-primary/50"}`}
                        onClick={() => handleTogglePlatform("local")}
                      >
                        <CardContent className="p-4 flex items-center justify-between">
                          <div className="flex items-center gap-3">
                            <Laptop
                              className={`h-5 w-5 ${formData.platforms.includes("local") ? "text-primary" : "text-muted-foreground"}`}
                            />
                            <span className="font-medium">FreelanceHub Only</span>
                          </div>
                          <Checkbox checked={formData.platforms.includes("local")} />
                        </CardContent>
                      </Card>
                    </div>

                    <div className="rounded-lg bg-muted p-4 flex items-start gap-3">
                      <AlertCircle className="h-5 w-5 text-primary mt-0.5" />
                      <div>
                        <h4 className="font-medium mb-1">Platform Account Connection</h4>
                        <p className="text-sm text-muted-foreground">
                          You need to connect your accounts for selected platforms before publishing. You can do this in
                          your account settings or when you publish.
                        </p>
                      </div>
                    </div>
                  </div>

                  <div className="rounded-lg bg-primary/10 p-4 space-y-3">
                    <h3 className="font-medium">AI-Powered Suggestions</h3>
                    <div className="space-y-2">
                      <div className="flex items-start gap-3">
                        <Star className="h-5 w-5 text-primary mt-0.5" />
                        <p className="text-sm">
                          Consider adding a video introduction to increase your conversion rate by up to 30%.
                        </p>
                      </div>
                      <div className="flex items-start gap-3">
                        <FileText className="h-5 w-5 text-primary mt-0.5" />
                        <p className="text-sm">
                          Your description is good, but adding specific examples of past work would make it stronger.
                        </p>
                      </div>
                      <div className="flex items-start gap-3">
                        <DollarSign className="h-5 w-5 text-primary mt-0.5" />
                        <p className="text-sm">
                          Based on market research, your premium tier could be priced 15-20% higher.
                        </p>
                      </div>
                    </div>
                  </div>
                </CardContent>
                <CardFooter className="flex justify-between">
                  <Button type="button" variant="outline" onClick={() => setActiveTab("description")}>
                    Back to Description
                  </Button>
                  <Button type="submit" disabled={isLoading}>
                    {isLoading ? (
                      <>
                        <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                        Creating Gig...
                      </>
                    ) : (
                      "Create & Publish Gig"
                    )}
                  </Button>
                </CardFooter>
              </Card>
            </TabsContent>
          </form>
        </Tabs>
      </div>
    </div>
  )
}

