from ControlIndex import ControlIndex
from IndexSegment import IndexSegment
from Page import Page
from Constants import *


class PartialReplication(object):
    def __init__(self, tree):
        self.__tree = tree
        self.__indexes = []
        self.__current_index_segment = None
        self.__pages = []

    def generate_broadcast(self):
        print "\n\nThe tree has %d levels excluding root." % self.__tree.get_tree_levels()
        self.__tree.set_replication_level(int(raw_input("Enter the replication level:")))
        print "\n\nGenerating Broadcast:                Started"
        print "Creating Index and Data Segments:    Started"
        self.__create_indexes(self.__tree.get_root())
        print "Creating Index and Data Segments:    Finished"
        print "Cleaning Index and Data Segments:    Started"
        self.__clean_indexes()
        print "Cleaning Index and Data Segments:    Finished"
        self.__generate_pages()
        self.__calculate_control_indexes()
        print "Generating Broadcast:                Finished"
        self.__run()

    def __clean_indexes(self):
        replication_level = self.__tree.get_replication_level()
        replication_node = self.__indexes[0].get_nodes()[replication_level]
        i = 1
        while i < len(self.__indexes):
            nodes = self.__indexes[i].get_nodes()
            if nodes[replication_level] is replication_node:
                for j in range(replication_level):
                    del nodes[j]
            else:
                replication_node = nodes[replication_level]

            i += 1

    def __create_indexes(self, node):
        nodes = node.get_children()
        if node.are_children_leafs():
            self.__current_index_segment = IndexSegment()
            self.__indexes.append(self.__current_index_segment)
            nodes.reverse()
            it = iter(nodes)
            for i in it:
                self.__current_index_segment.add_index_item(i)
            nodes.reverse()
            self.__current_index_segment.add_index_item(node)
            pnode = node.get_parent_node()
            while pnode is not None:
                self.__current_index_segment.add_index_item(pnode)
                pnode = pnode.get_parent_node()
            self.__current_index_segment.reverse()
            self.__current_index_segment.complete_data()
        else:
            it = iter(nodes)
            for i in it:
                self.__create_indexes(i)

    def __generate_pages(self):
        print "Generating BroadCast Pages:          Started"
        self.__pages = []
        it = iter(self.__indexes)
        for i in it:
            jt = iter(i.get_nodes())
            for j in jt:
                p = Page(j.get_name(), INDEX_TYPE)
                self.__pages.append(p)
            dt = iter(i.get_data_segment().get_data())
            for d in dt:
                p = Page(d.get_name(), DATA_TYPE)
                p.set_data(d.get_data())
                p.set_name(d.get_name())
                self.__pages.append(p)

        for i in range(len(self.__pages)):
            found = False
            count = 0
            for j in range(len(self.__pages)):
                if (self.__pages[i].get_type() == INDEX_TYPE) and (self.__pages[i].get_name() == self.__pages[j].get_name()):
                    found = True
                    count += 1

            if found and (count > 1):
                name = self.__pages[i].get_name()
                count = 1
                for j in range(i, len(self.__pages)):
                    if (self.__pages[j].get_type() == INDEX_TYPE) and (name == self.__pages[j].get_name()):
                        self.__pages[j].set_name(name + '-' + str(count))
                        self.__pages[j].set_type(INDEX_TYPE)
                        count += 1

        print "Generating BroadCast Pages:          Finished"

    def __calculate_control_indexes(self):
        print "Calculating Page Control Indices:    Started"
        name = self.__pages[0].get_name().split('-')[0]
        root_pages = []
        root_data = []

        for i in range(len(self.__pages)):
            if (i > 0) and (self.__pages[i].get_type() == INDEX_TYPE) and (name == self.__pages[i].get_name().split('-')[0]):
                root_pages.append(self.__pages[i])
                root_data.append(self.__pages[i-1])

        for i in range(len(root_pages)):
            ci = ControlIndex()
            ci.set_lower_bound(root_data[i])
            ci.set_lower_bound_next(self.__pages[0])
            root_pages[i].set_control_index(ci)

        for i in range(len(self.__pages)):
            tmp_name = self.__pages[i].get_name().split('-')
            if (len(tmp_name) > 1) and (tmp_name[0] != name) and (self.__pages[i].get_control_index() is None):
                j = i - 1
                data = None
                ci = ControlIndex()
                while j >= 0:
                    if self.__pages[j].get_type() == DATA_TYPE:
                        data = self.__pages[j]
                        break
                    j -= 1
                if data is not None:
                    ci.set_lower_bound(data)
                    ci.set_lower_bound_next(self.__pages[0])

                j = i + 1
                root = None
                while j < len(self.__pages):
                    tmp_name = self.__pages[j].get_name().split('-')
                    if (len(tmp_name) > 1) and (tmp_name[0] == name):
                        root = self.__pages[j]
                        break
                    j += 1
                if root is not None:
                    ci.set_upper_bound(self.__pages[j - 1])
                    ci.set_upper_bound_next(root)
                else:
                    ci.set_upper_bound(self.__pages[len(self.__pages) - 1])
                    ci.set_upper_bound_next(self.__pages[0])

                self.__pages[i].set_control_index(ci)

        self.__calculate_data_indexes()
        self.__calculate_index_offsets()

        for i in range(1, len(self.__pages)):
            if self.__pages[i].get_control_index() is None:
                j = i - 1
                data = None
                ci = ControlIndex()
                while j >= 0:
                    if self.__pages[j].get_type() == DATA_TYPE:
                        data = self.__pages[j]
                        break
                    j -= 1
                if data is not None:
                    ci.set_lower_bound(data)
                    ci.set_lower_bound_next(self.__pages[0])

                j = i + 1
                while j < len(self.__pages):
                    if self.__pages[j].get_type() == DATA_TYPE:
                        break
                    j += 1
                root = None
                while j < len(self.__pages):
                    if self.__pages[j].get_type() == INDEX_TYPE:
                        root = self.__pages[j]
                        break
                    j += 1
                if root is not None:
                    ci.set_upper_bound(self.__pages[j - 1])
                    ci.set_upper_bound_next(root)
                else:
                    ci.set_upper_bound(self.__pages[len(self.__pages) - 1])
                    ci.set_upper_bound_next(self.__pages[0])

                self.__pages[i].set_control_index(ci)

        print "Calculating Page Control Indices:    Finished"

    def __calculate_data_indexes(self):
        for i in range(len(self.__pages)):
            if self.__pages[i].get_type() == DATA_TYPE:
                j = i + 1
                while j < (len(self.__pages) - 1):
                    if self.__pages[j].get_type() == INDEX_TYPE:
                        self.__pages[i].set_index(self.__pages[j])
                        break
                    j += 1
                if self.__pages[i].get_index() is None:
                    self.__pages[i].set_index(self.__pages[0])

    def __calculate_index_offsets(self):
        i = 1
        while i < len(self.__pages):
            if self.__pages[i].get_type() == DATA_TYPE:
                j = i
                i -= 1
                while j < len(self.__pages):
                    if self.__pages[j].get_type() == INDEX_TYPE:
                        break
                    j += 1
                next_index_pos = j
                j -= 1
                while self.__pages[j].get_type() == DATA_TYPE:
                    self.__pages[i].set_data_offset(self.__pages[j])
                    j -= 1
                    i -= 1

                i = next_index_pos
            else:
                i += 1

    def __pretty_print(self, page):
        pretty_print = '\n\n|'
        name = self.__pages[0].get_name().split('-')
        for i in range(len(self.__pages)):
            tmp_name = self.__pages[i].get_name().split('-')
            if i == 0:
                if (page is not None) and (page.get_name() == self.__pages[i].get_name()):
                    pretty_print = pretty_print + '** ' + self.__pages[i].get_name() + ' **' + '|'
                else:
                    pretty_print = pretty_print + self.__pages[i].get_name() + '|'
            elif (i > 0) and (tmp_name[0] != name[0]):
                if (page is not None) and (page.get_name() == self.__pages[i].get_name()):
                    pretty_print = pretty_print + '** ' + self.__pages[i].get_name() + ' **' + '|'
                else:
                    pretty_print = pretty_print + self.__pages[i].get_name() + '|'
            else:
                print "%s" % pretty_print
                if (page is not None) and (page.get_name() == self.__pages[i].get_name()):
                    pretty_print = '|' + '** ' + self.__pages[i].get_name() + ' **' + '|'
                else:
                    pretty_print = '|' + self.__pages[i].get_name() + '|'
        print "%s\n\n" % pretty_print

    def __run(self):
        self.__pretty_print(None)
        a = raw_input("Enter data to seek:")
        while len(a) > 0:
            b = raw_input("Enter where to start:")
            print "\nThe current page name will be surrounded by '**'s"
            j = 0
            for i in range(len(self.__pages)):
                if b == self.__pages[i].get_name():
                    j = i
                    break
            p = self.__pages[j]
            found = False
            self.__pretty_print(p)
            raw_input("Pausing....press enter to continue")
            while not found:
                if p.get_type() == DATA_TYPE:
                    if p.get_name() == a:
                        found = True
                    else:
                        p = p.get_index()
                elif p.get_type() == INDEX_TYPE:
                    if p.get_data_offset() is not None:
                        if p.get_data_offset().get_name() == a:
                            p = p.get_data_offset()
                        else:
                            i = 0
                            while i < len(self.__pages):
                                if p is self.__pages[i]:
                                    p = self.__pages[i + 1]
                                    break
                                i += 1
                    elif p.get_control_index() is None:
                        i = 0
                        while i < len(self.__pages):
                            if p is self.__pages[i]:
                                p = self.__pages[i + 1]
                                break
                            i += 1
                    else:
                        got_it = False
                        if p.get_control_index().get_lower_bound() is not None:
                            if int(a) <= int(p.get_control_index().get_lower_bound().get_name()):
                                p = p.get_control_index().get_lower_bound_next()
                                got_it = True
                        if not got_it:
                            if p.get_control_index().get_upper_bound() is not None:
                                if int(a) > int(p.get_control_index().get_upper_bound().get_name()):
                                    p = p.get_control_index().get_upper_bound_next()
                                    got_it = True

                        if not got_it:
                            i = 0
                            while i < len(self.__pages):
                                if p is self.__pages[i]:
                                    p = self.__pages[i + 1]
                                    break
                                i += 1
                if not found:
                    self.__pretty_print(p)
                    raw_input("Pausing....press enter to continue")
            a = raw_input("Enter data to seek:")
