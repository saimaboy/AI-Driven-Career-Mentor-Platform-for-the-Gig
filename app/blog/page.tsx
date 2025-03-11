import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Tabs, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { BookOpen, Clock, Search, Tag } from "lucide-react"

export default function BlogPage() {
  return (
    <div className="container py-10">
      <div className="flex flex-col space-y-6">
        <div className="flex flex-col space-y-2">
          <h1 className="text-3xl font-bold">Freelance Knowledge Hub</h1>
          <p className="text-muted-foreground">Insights, tips, and resources to help you succeed as a freelancer</p>
        </div>

        <div className="flex flex-col md:flex-row gap-4">
          <div className="relative w-full md:w-2/3">
            <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
            <Input type="search" placeholder="Search articles..." className="w-full pl-8" />
          </div>
          <div className="w-full md:w-1/3">
            <Tabs defaultValue="all">
              <TabsList className="grid w-full grid-cols-4">
                <TabsTrigger value="all">All</TabsTrigger>
                <TabsTrigger value="guides">Guides</TabsTrigger>
                <TabsTrigger value="tips">Tips</TabsTrigger>
                <TabsTrigger value="news">News</TabsTrigger>
              </TabsList>
            </Tabs>
          </div>
        </div>

        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          <Card>
            <CardHeader className="pb-2">
              <div className="flex items-center gap-2 text-sm text-muted-foreground mb-2">
                <Tag className="h-4 w-4" />
                <span>Freelance Tips</span>
                <span className="mx-1">•</span>
                <Clock className="h-4 w-4" />
                <span>5 min read</span>
              </div>
              <CardTitle className="text-xl">How to Set Your Freelance Rates: A Comprehensive Guide</CardTitle>
              <CardDescription>
                Learn how to price your services effectively to maximize earnings without scaring away clients.
              </CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground">
                Setting the right rates is one of the most challenging aspects of freelancing. This guide walks you
                through different pricing strategies and helps you find the sweet spot for your services.
              </p>
            </CardContent>
            <CardFooter>
              <Link href="/blog/how-to-set-freelance-rates" className="w-full">
                <Button variant="outline" className="w-full">
                  <BookOpen className="mr-2 h-4 w-4" />
                  Read Article
                </Button>
              </Link>
            </CardFooter>
          </Card>

          <Card>
            <CardHeader className="pb-2">
              <div className="flex items-center gap-2 text-sm text-muted-foreground mb-2">
                <Tag className="h-4 w-4" />
                <span>Client Management</span>
                <span className="mx-1">•</span>
                <Clock className="h-4 w-4" />
                <span>7 min read</span>
              </div>
              <CardTitle className="text-xl">10 Red Flags to Watch for When Taking on New Clients</CardTitle>
              <CardDescription>
                Identify problematic clients before they become a headache and protect your freelance business.
              </CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground">
                Not all clients are created equal. Learn to spot the warning signs of difficult clients early on and
                save yourself from stress, scope creep, and payment issues.
              </p>
            </CardContent>
            <CardFooter>
              <Link href="/blog/client-red-flags" className="w-full">
                <Button variant="outline" className="w-full">
                  <BookOpen className="mr-2 h-4 w-4" />
                  Read Article
                </Button>
              </Link>
            </CardFooter>
          </Card>

          <Card>
            <CardHeader className="pb-2">
              <div className="flex items-center gap-2 text-sm text-muted-foreground mb-2">
                <Tag className="h-4 w-4" />
                <span>Productivity</span>
                <span className="mx-1">•</span>
                <Clock className="h-4 w-4" />
                <span>6 min read</span>
              </div>
              <CardTitle className="text-xl">The Freelancer's Guide to Time Management and Productivity</CardTitle>
              <CardDescription>
                Maximize your efficiency and output with these proven strategies for freelancers.
              </CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground">
                When you're a freelancer, time literally equals money. Discover practical techniques to manage your
                schedule, minimize distractions, and get more done in less time.
              </p>
            </CardContent>
            <CardFooter>
              <Link href="/blog/freelancer-time-management" className="w-full">
                <Button variant="outline" className="w-full">
                  <BookOpen className="mr-2 h-4 w-4" />
                  Read Article
                </Button>
              </Link>
            </CardFooter>
          </Card>

          <Card>
            <CardHeader className="pb-2">
              <div className="flex items-center gap-2 text-sm text-muted-foreground mb-2">
                <Tag className="h-4 w-4" />
                <span>Marketing</span>
                <span className="mx-1">•</span>
                <Clock className="h-4 w-4" />
                <span>8 min read</span>
              </div>
              <CardTitle className="text-xl">Building Your Personal Brand as a Freelancer</CardTitle>
              <CardDescription>
                Stand out in a crowded marketplace by developing a strong personal brand.
              </CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground">
                Your personal brand is what sets you apart from the competition. Learn how to craft a compelling brand
                story, create a consistent online presence, and attract your ideal clients.
              </p>
            </CardContent>
            <CardFooter>
              <Link href="/blog/freelancer-personal-branding" className="w-full">
                <Button variant="outline" className="w-full">
                  <BookOpen className="mr-2 h-4 w-4" />
                  Read Article
                </Button>
              </Link>
            </CardFooter>
          </Card>

          <Card>
            <CardHeader className="pb-2">
              <div className="flex items-center gap-2 text-sm text-muted-foreground mb-2">
                <Tag className="h-4 w-4" />
                <span>Finance</span>
                <span className="mx-1">•</span>
                <Clock className="h-4 w-4" />
                <span>10 min read</span>
              </div>
              <CardTitle className="text-xl">Tax Tips Every Freelancer Should Know</CardTitle>
              <CardDescription>
                Navigate the complexities of freelance taxes and maximize your deductions.
              </CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground">
                Tax season doesn't have to be stressful. This comprehensive guide covers everything from quarterly
                estimated payments to home office deductions and retirement planning.
              </p>
            </CardContent>
            <CardFooter>
              <Link href="/blog/freelancer-tax-tips" className="w-full">
                <Button variant="outline" className="w-full">
                  <BookOpen className="mr-2 h-4 w-4" />
                  Read Article
                </Button>
              </Link>
            </CardFooter>
          </Card>

          <Card>
            <CardHeader className="pb-2">
              <div className="flex items-center gap-2 text-sm text-muted-foreground mb-2">
                <Tag className="h-4 w-4" />
                <span>Growth</span>
                <span className="mx-1">•</span>
                <Clock className="h-4 w-4" />
                <span>9 min read</span>
              </div>
              <CardTitle className="text-xl">From Freelancer to Agency: Scaling Your Business</CardTitle>
              <CardDescription>
                Ready to grow beyond solo freelancing? Learn how to build a team and scale your operations.
              </CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground">
                Transitioning from a solo freelancer to a small agency comes with unique challenges. This guide covers
                hiring, delegation, systems, and everything you need to scale successfully.
              </p>
            </CardContent>
            <CardFooter>
              <Link href="/blog/scaling-freelance-business" className="w-full">
                <Button variant="outline" className="w-full">
                  <BookOpen className="mr-2 h-4 w-4" />
                  Read Article
                </Button>
              </Link>
            </CardFooter>
          </Card>
        </div>

        <div className="flex justify-center">
          <Button variant="outline">Load More Articles</Button>
        </div>

        <div className="rounded-lg border p-6 mt-6">
          <div className="flex flex-col items-center text-center space-y-4">
            <h2 className="text-2xl font-bold">Subscribe to Our Newsletter</h2>
            <p className="text-muted-foreground max-w-[600px]">
              Get the latest freelancing tips, resources, and opportunities delivered straight to your inbox.
            </p>
            <div className="flex w-full max-w-md gap-2">
              <Input type="email" placeholder="Enter your email" />
              <Button>Subscribe</Button>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

