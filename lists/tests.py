from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from lists.views import home_page
from django.template.loader import render_to_string
from lists.models import Item, List
# Create your tests here.

class HomePageTest(TestCase):
    
    def test_root_url_resolves_to_home_page_view(self):
        """
        测试访问路径"/"是否由home_page函数处理
        """
        found = resolve('/')
        self.assertEqual(found.func,home_page)

    def test_home_page_returns_correct_html(self):
        """
        测试home_page函数是否返回了正确的相应
        """
        request = HttpRequest()
        response = home_page(request)
        expected_html = render_to_string('home.html')
        self.assertEqual(response.content.decode(),expected_html)

class ListViewTest(TestCase):
    def test_uses_list_template(self):
        """
        测试/lists/the-only-list-in-the-world的处理函数的返回是否使用了list.html模版
        """
        list_ = List.objects.create()
        response = self.client.get('/lists/%d/'%(list_.id,))
        self.assertTemplateUsed(response, 'list.html')

    def test_displays_only_items_for_that_list(self):
        """
        测试/lists/the-only-list-in-the-world的处理函数的返回是否包含数据项Item的值
        """
        correct_list = List.objects.create()
        Item.objects.create(text='itemey 1', list=correct_list)
        Item.objects.create(text='itemey 2', list=correct_list)
        
        other_list = List.objects.create()
        Item.objects.create(text='other list item 1', list=other_list)
        Item.objects.create(text='other list item 2', list=other_list)

        response = self.client.get('/lists/%d/'%(correct_list.id,))

        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')
        self.assertNotContains(response, 'other list item 1')
        self.assertNotContains(response, 'other list item 2')


    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get('/lists/%d/' %(correct_list.id,))
        self.assertEqual(response.context['list'], correct_list)

class NewListTest(TestCase):

    def test_saving_a_POST_request(self):
        """
        测试POST /lists/new的返回是否包含数据项Item
        """
        self.client.post(
                '/lists/new',
                data = {'item_text': 'A new list item'}
            )
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirects_after_POST(self):
        """
        测试POST /lists/new成功后是否REDIRECT，且判断REDIRECT页面是否正确
        """
        response = self.client.post(
                '/lists/new',
                data = {'item_text': 'A new list item'}
            )
        new_list = List.objects.first()
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/lists/%d/'%(new_list.id,))

class ListAndItemModelTest(TestCase):
    def test_saving_and_retrieving_items(self):
        list_ = List()
        list_.save()

        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.list = list_
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.list = list_
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(first_saved_item.list, list_)
        self.assertEqual(second_saved_item.text, 'Item the second')
        self.assertEqual(second_saved_item.list, list_)

class NewItemTest(TestCase):
    def test_can_save_a_POST_request_to_an_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(
                '/lists/%d/add_item' % (correct_list.id,),
                data = {'item_text': 'A new item for an existing list'}
                )

        self.assertEqual(Item.objects.count(),1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item for an existing list')
        self.assertEqual(new_item.list, correct_list)

    def test_redirect_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(
                '/lists/%d/add_item' % (correct_list.id,),
                data = {'item_text': 'A new item for an existing list'}
                )

        self.assertRedirects(response, '/lists/%d/' % (correct_list.id,))
        

    
