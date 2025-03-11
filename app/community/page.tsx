"use client"

import type React from "react"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Badge } from "@/components/ui/badge"
import { Textarea } from "@/components/ui/textarea"
import { MessageSquare, Search, ThumbsUp, Users } from "lucide-react"

export default function CommunityPage() {
  const [activeTab, setActiveTab] = useState("discussions")
  const [postContent, setPostContent] = useState("")

  const handlePostSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    console.log("Post submitted:", postContent)
    setPostContent("")
    // Here you would typically send this to your backend
  }

  return (
    <div className="container py-10">
      <div className="flex flex-col space-y-6">
        <div className="flex flex-col space-y-2">
          <h1 className="text-3xl font-bold">Freelancer Community</h1>
          <p className="text-muted-foreground">Connect with other freelancers, share knowledge, and grow together</p>
        </div>

        <div className="flex flex-col md:flex-row gap-6">
          <div className="w-full md:w-3/4">
            <Tabs defaultValue="discussions" value={activeTab} onValueChange={setActiveTab} className="space-y-4">
              <div className="flex items-center justify-between">
                <TabsList>
                  <TabsTrigger value="discussions">Discussions</TabsTrigger>
                  <TabsTrigger value="questions">Questions</TabsTrigger>
                  <TabsTrigger value="showcase">Showcase</TabsTrigger>
                  <TabsTrigger value="jobs">Job Board</TabsTrigger>
                </TabsList>
                <div className="relative hidden md:block w-[200px]">
                  <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
                  <Input type="search" placeholder="Search..." className="pl-8" />
                </div>
              </div>

              <Card>
                <CardHeader className="pb-3">
                  <CardTitle>Create a Post</CardTitle>
                  <CardDescription>Share your thoughts, ask questions, or showcase your work</CardDescription>
                </CardHeader>
                <CardContent>
                  <form onSubmit={handlePostSubmit}>
                    <Textarea
                      placeholder="What's on your mind?"
                      className="mb-3"
                      value={postContent}
                      onChange={(e) => setPostContent(e.target.value)}
                    />
                    <div className="flex justify-end">
                      <Button type="submit" disabled={!postContent.trim()}>
                        Post
                      </Button>
                    </div>
                  </form>
                </CardContent>
              </Card>

              <TabsContent value="discussions" className="space-y-4 mt-0">
                <Card>
                  <CardHeader className="pb-3">
                    <div className="flex justify-between">
                      <div className="flex items-center space-x-4">
                        <Avatar>
                          <AvatarImage src="/placeholder.svg" />
                          <AvatarFallback>JD</AvatarFallback>
                        </Avatar>
                        <div>
                          <p className="text-sm font-medium">Jane Doe</p>
                          <p className="text-xs text-muted-foreground">Posted 2 hours ago</p>
                        </div>
                      </div>
                      <Badge>Discussion</Badge>
                    </div>
                  </CardHeader>
                  <CardContent>
                    <h3 className="text-lg font-semibold mb-2">How do you handle scope creep with clients?</h3>
                    <p className="text-sm text-muted-foreground">
                      I'm working with a client who keeps adding "small changes" to the project. These are starting to
                      add up and I'm not sure how to address it without damaging the relationship. Any advice from
                      experienced freelancers?
                    </p>
                  </CardContent>
                  <CardFooter className="border-t px-6 py-3">
                    <div className="flex items-center space-x-4">
                      <Button variant="ghost" size="sm" className="gap-1">
                        <ThumbsUp className="h-4 w-4" />
                        <span>24</span>
                      </Button>
                      <Button variant="ghost" size="sm" className="gap-1">
                        <MessageSquare className="h-4 w-4" />
                        <span>18 Comments</span>
                      </Button>
                    </div>
                  </CardFooter>
                </Card>

                <Card>
                  <CardHeader className="pb-3">
                    <div className="flex justify-between">
                      <div className="flex items-center space-x-4">
                        <Avatar>
                          <AvatarImage src="/placeholder.svg" />
                          <AvatarFallback>MS</AvatarFallback>
                        </Avatar>
                        <div>
                          <p className="text-sm font-medium">Michael Smith</p>
                          <p className="text-xs text-muted-foreground">Posted yesterday</p>
                        </div>
                      </div>
                      <Badge>Discussion</Badge>
                    </div>
                  </CardHeader>
                  <CardContent>
                    <h3 className="text-lg font-semibold mb-2">Best invoicing software for freelancers?</h3>
                    <p className="text-sm text-muted-foreground">
                      I'm looking to upgrade my invoicing system. Currently using spreadsheets but it's getting unwieldy
                      as my client base grows. What software do you recommend that's affordable but professional?
                    </p>
                  </CardContent>
                  <CardFooter className="border-t px-6 py-3">
                    <div className="flex items-center space-x-4">
                      <Button variant="ghost" size="sm" className="gap-1">
                        <ThumbsUp className="h-4 w-4" />
                        <span>32</span>
                      </Button>
                      <Button variant="ghost" size="sm" className="gap-1">
                        <MessageSquare className="h-4 w-4" />
                        <span>26 Comments</span>
                      </Button>
                    </div>
                  </CardFooter>
                </Card>

                <Card>
                  <CardHeader className="pb-3">
                    <div className="flex justify-between">
                      <div className="flex items-center space-x-4">
                        <Avatar>
                          <AvatarImage src="/placeholder.svg" />
                          <AvatarFallback>AJ</AvatarFallback>
                        </Avatar>
                        <div>
                          <p className="text-sm font-medium">Alex Johnson</p>
                          <p className="text-xs text-muted-foreground">Posted 3 days ago</p>
                        </div>
                      </div>
                      <Badge>Discussion</Badge>
                    </div>
                  </CardHeader>
                  <CardContent>
                    <h3 className="text-lg font-semibold mb-2">How to balance multiple projects effectively?</h3>
                    <p className="text-sm text-muted-foreground">
                      I've recently taken on several clients simultaneously and I'm struggling to manage my time
                      effectively. How do you all handle multiple projects without burning out or missing deadlines?
                    </p>
                  </CardContent>
                  <CardFooter className="border-t px-6 py-3">
                    <div className="flex items-center space-x-4">
                      <Button variant="ghost" size="sm" className="gap-1">
                        <ThumbsUp className="h-4 w-4" />
                        <span>45</span>
                      </Button>
                      <Button variant="ghost" size="sm" className="gap-1">
                        <MessageSquare className="h-4 w-4" />
                        <span>37 Comments</span>
                      </Button>
                    </div>
                  </CardFooter>
                </Card>

                <div className="flex justify-center">
                  <Button variant="outline">Load More</Button>
                </div>
              </TabsContent>

              <TabsContent value="questions" className="space-y-4 mt-0">
                <Card>
                  <CardContent className="pt-6">
                    <p className="text-center text-muted-foreground">Questions tab content will appear here</p>
                  </CardContent>
                </Card>
              </TabsContent>

              <TabsContent value="showcase" className="space-y-4 mt-0">
                <Card>
                  <CardContent className="pt-6">
                    <p className="text-center text-muted-foreground">Showcase tab content will appear here</p>
                  </CardContent>
                </Card>
              </TabsContent>

              <TabsContent value="jobs" className="space-y-4 mt-0">
                <Card>
                  <CardContent className="pt-6">
                    <p className="text-center text-muted-foreground">Job Board tab content will appear here</p>
                  </CardContent>
                </Card>
              </TabsContent>
            </Tabs>
          </div>

          <div className="w-full md:w-1/4 space-y-4">
            <Card>
              <CardHeader>
                <CardTitle>Community Stats</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  <div className="flex justify-between">
                    <span className="text-sm">Members</span>
                    <span className="text-sm font-medium">12,458</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm">Online Now</span>
                    <span className="text-sm font-medium">342</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm">Topics</span>
                    <span className="text-sm font-medium">3,721</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm">Posts Today</span>
                    <span className="text-sm font-medium">87</span>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Active Members</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="flex items-center space-x-3">
                    <Avatar>
                      <AvatarImage src="/placeholder.svg" />
                      <AvatarFallback>JD</AvatarFallback>
                    </Avatar>
                    <div>
                      <p className="text-sm font-medium">Jane Doe</p>
                      <p className="text-xs text-muted-foreground">Web Developer</p>
                    </div>
                  </div>
                  <div className="flex items-center space-x-3">
                    <Avatar>
                      <AvatarImage src="/placeholder.svg" />
                      <AvatarFallback>MS</AvatarFallback>
                    </Avatar>
                    <div>
                      <p className="text-sm font-medium">Michael Smith</p>
                      <p className="text-xs text-muted-foreground">Graphic Designer</p>
                    </div>
                  </div>
                  <div className="flex items-center space-x-3">
                    <Avatar>
                      <AvatarImage src="/placeholder.svg" />
                      <AvatarFallback>AJ</AvatarFallback>
                    </Avatar>
                    <div>
                      <p className="text-sm font-medium">Alex Johnson</p>
                      <p className="text-xs text-muted-foreground">Content Writer</p>
                    </div>
                  </div>
                  <div className="flex items-center space-x-3">
                    <Avatar>
                      <AvatarImage src="/placeholder.svg" />
                      <AvatarFallback>SL</AvatarFallback>
                    </Avatar>
                    <div>
                      <p className="text-sm font-medium">Sarah Lee</p>
                      <p className="text-xs text-muted-foreground">UI/UX Designer</p>
                    </div>
                  </div>
                  <div className="flex items-center space-x-3">
                    <Avatar>
                      <AvatarImage src="/placeholder.svg" />
                      <AvatarFallback>RB</AvatarFallback>
                    </Avatar>
                    <div>
                      <p className="text-sm font-medium">Robert Brown</p>
                      <p className="text-xs text-muted-foreground">Marketing Specialist</p>
                    </div>
                  </div>
                </div>
              </CardContent>
              <CardFooter>
                <Button variant="ghost" size="sm" className="w-full">
                  <Users className="mr-2 h-4 w-4" />
                  View All Members
                </Button>
              </CardFooter>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Popular Topics</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="flex flex-wrap gap-2">
                  <Badge variant="secondary">Pricing</Badge>
                  <Badge variant="secondary">Client Management</Badge>
                  <Badge variant="secondary">Web Development</Badge>
                  <Badge variant="secondary">Design</Badge>
                  <Badge variant="secondary">Marketing</Badge>
                  <Badge variant="secondary">Taxes</Badge>
                  <Badge variant="secondary">Contracts</Badge>
                  <Badge variant="secondary">Productivity</Badge>
                  <Badge variant="secondary">Work-Life Balance</Badge>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  )
}

