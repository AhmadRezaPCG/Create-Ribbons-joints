###############################################################################
# Name: 
#   Create ribbon joint
#
# Description: 
#   By this script you can create faster and easily a ribbons joint with offset CTL and driver CTL . in this method i used a NURBS surface that it skinbind to the driver jnt (if your driver button was checked )and then with UVpin constraint ,the follower jnt UVpin constraint to the ribbon .
#      By driver jnt you can control all of the joint in a joint chain .
#      this method used by Taylor Whitsett at Character Rigging In Maya For Game Production workshop . 
#      I hope you use and enjoy it . 
#   
#
# Author: 
#   Ahmadreza Rezaei
#
# Copyright (C) 2022 Ahmadreza Rezaei. All rights reserved.
###############################################################################


import maya.cmds as cmds
import maya.OpenMayaUI as omui
import maya.OpenMaya as om

from PySide2 import QtCore
from PySide2 import QtWidgets
from shiboken2 import wrapInstance

def maya_main_window():
    main_window = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window),QtWidgets.QWidget)
    
class createribbonsjnt(QtWidgets.QDialog):
    
    dialog_window = None
    
    def __init__(self,parent=maya_main_window()):
        super(createribbonsjnt,self).__init__(parent)
        
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
        
        self.setWindowTitle("Ribbons joint")
        
        self.createwidget()
        self.createlayout()
        self.connectsignalslot()
    
    @classmethod
    def show_dialog(cls):
        if cls.dialog_window:
            if cls.dialog_window.isHidden():
                cls.dialog_window.show()
            else:
                cls.dialog_window.raise_()
                cls.dialog_window.activateWindow()
        else:
            cls.dialog_window = createribbonsjnt()
            cls.dialog_window.show()
    
    def createwidget(self):
        
        
        self.LE_startjnt = QtWidgets.QLineEdit()
        self.LE_startjnt.setPlaceholderText("Start Jnt")
        self.LE_startjnt.setEnabled(False)
        self.LE_endjnt = QtWidgets.QLineEdit()
        self.LE_endjnt.setPlaceholderText("End JNT")
        self.LE_endjnt.setEnabled(False)
        
        self.PB_setjnt = QtWidgets.QPushButton("Set Joints")
        
        self.L_sidejnt = QtWidgets.QLabel("Side view : ")
        self.RB_x = QtWidgets.QRadioButton("X")
        self.RB_x.setChecked(True)
        self.RB_y = QtWidgets.QRadioButton("Y")
        self.RB_z = QtWidgets.QRadioButton("Z")
        self.CB_reverse = QtWidgets.QComboBox()
        self.CB_reverse.setEditable(False)
        self.CB_reverse.addItem("-")
        self.CB_reverse.addItem("+")
        
        
        self.CB_createfollowerjnt = QtWidgets.QCheckBox("Follower Joint")
        self.CB_createoffsetctl = QtWidgets.QCheckBox("offset ctl")
        
        self.CB_createdriverjoint =QtWidgets.QCheckBox("Driver jnt")
        self.CB_createdriverjoint.setChecked(False)
        self.IS_numbdriverjnt = QtWidgets.QSpinBox()
        self.IS_numbdriverjnt.setEnabled(False)
        self.IS_numbdriverjnt.setEnabled(False)
        self.CB_uvpin = QtWidgets.QCheckBox("UV Pin")
        self.CB_uvpin.setEnabled(False)
        self.CB_uvpin.setChecked(False)
        self.CB_createctldriver = QtWidgets.QCheckBox("CTL driver")
        self.CB_createctldriver.setChecked(False)
        self.CB_createctldriver.setEnabled(False)
        
        self.PB_cancel = QtWidgets.QPushButton("Cancel")
        self.PB_create = QtWidgets.QPushButton("Create")
    
    def createlayout(self):
        
        VL_setjnt = QtWidgets.QVBoxLayout()
        
        HL_lineedit = QtWidgets.QHBoxLayout()
        HL_lineedit.addWidget(self.LE_startjnt)
        HL_lineedit.addWidget(self.LE_endjnt)
        
        HL_selectside = QtWidgets.QHBoxLayout()
        HL_selectside.addWidget(self.L_sidejnt)
        HL_selectside.addWidget(self.RB_x)
        HL_selectside.addWidget(self.RB_y)
        HL_selectside.addWidget(self.RB_z)
        HL_selectside.addWidget(self.CB_reverse)
        
        VL_setjnt.addLayout(HL_lineedit)
        VL_setjnt.addWidget(self.PB_setjnt)
        VL_setjnt.addLayout(HL_selectside)
        
        FL_DS = QtWidgets.QFormLayout()
        FL_DS.addRow("Count driver joint",self.IS_numbdriverjnt)
        
        HL_bottombutton = QtWidgets.QHBoxLayout()
        HL_bottombutton.addWidget(self.PB_create)
        HL_bottombutton.addStretch()
        HL_bottombutton.addWidget(self.PB_cancel)
        
        frame_1 = QtWidgets.QFrame()
        frame_1.setFrameShape(QtWidgets.QFrame.HLine)
        frame_1.setLineWidth(10)
        
        frame_2 = QtWidgets.QFrame()
        frame_2.setFrameShape(QtWidgets.QFrame.HLine)
        frame_2.setLineWidth(10)
        
        frame_3 = QtWidgets.QFrame()
        frame_3.setFrameShape(QtWidgets.QFrame.HLine)
        frame_3.setLineWidth(10)
        
        
        MAIN_layout = QtWidgets.QVBoxLayout(self)
        MAIN_layout.addLayout(VL_setjnt)
        MAIN_layout.addWidget(frame_1)
        MAIN_layout.addWidget(self.CB_createfollowerjnt)
        MAIN_layout.addWidget(self.CB_createoffsetctl)
        MAIN_layout.addWidget(frame_2)
        MAIN_layout.addWidget(self.CB_createdriverjoint)
        MAIN_layout.addWidget(self.CB_uvpin)
        MAIN_layout.addLayout(FL_DS)
        MAIN_layout.addWidget(self.CB_createctldriver)
        MAIN_layout.addStretch()
        MAIN_layout.addWidget(frame_3)
        MAIN_layout.addLayout(HL_bottombutton)
        
        
        
    def connectsignalslot(self):
        
        self.PB_cancel.clicked.connect(self.close)
        self.PB_setjnt.clicked.connect(self.set_joint_to_lineedit)
        self.PB_create.clicked.connect(self.prepare_ribbon)
        self.CB_createfollowerjnt.toggled.connect(self.change_enable_uvpin)
        self.CB_createdriverjoint.toggled.connect(self.change_enable_driver)
        self.LE_startjnt.textChanged.connect(self.set_maxi_min_driver)
        self.LE_endjnt.textChanged.connect(self.set_maxi_min_driver)
        
    def change_enable_uvpin(self,toggle):
        
        if toggle:
            if self.CB_createdriverjoint.isChecked():
                self.CB_uvpin.setEnabled(True)
            else:
                self.CB_uvpin.setEnabled(False)
        else:
            self.CB_uvpin.setEnabled(False)
            
    def prepare_ribbon(self):
        
        self.check_line_edit_exist()
        side_joint = self.get_checkboxnormal()
        bool_followerjnt = self.CB_createfollowerjnt.isChecked()
        bool_offsetctl = self.CB_createoffsetctl.isChecked()
        bool_driverjnt = self.CB_createdriverjoint.isChecked()
        bool_uv_pin = self.CB_uvpin.isChecked()
        self.create_ribbon(side_joint,bool_followerjnt,bool_offsetctl,bool_driverjnt,bool_uv_pin)
        
        
    def change_enable_driver(self,toggle):
        
        try:
            self.start_long_name
        except:
            self.CB_createdriverjoint.setChecked(False)
            raise RuntimeError("First set your jnt . ")
        
        self.IS_numbdriverjnt.setEnabled(toggle)
        self.CB_createctldriver.setEnabled(toggle)
        self.CB_uvpin.setEnabled(toggle)
        
    def create_ribbon(self,side_joint,bool_followerjnt=False,bool_offsetctl=False,bool_driverjnt=False,bool_uv_pin=False):
        
        grps = self.create_grps()
        
        offset_ctl = grps[0]
        follower_jnt_grp = grps[1]
        nurbs_grp = grps[2]
        driver_ctl =grps[3]
        driver_jnt_grp = grps[4]
        main_grp = grps[5]
        
        self.create_follower_jnt(follower_jnt_grp)
        
        
        
        positions = self.get_positions_joints(follower_jnt_grp)
        name_loft = self.create_nurbs_loft(positions)
        cmds.parent(name_loft,nurbs_grp)
        name_loft =self.get_path_name(nurbs_grp,name_loft)
        
        self.create_attr_main(main_grp,"Nurbs",name_loft)
        self.create_attr_main(main_grp,"Offset_JNT",follower_jnt_grp)
        
        if bool_driverjnt:
            if bool_uv_pin:
                if bool_followerjnt:
                    self.create_uvpin(follower_jnt_grp,name_loft)
        
        if bool_offsetctl:
            self.create_offset(bool_followerjnt,follower_jnt_grp,offset_ctl)
            self.create_attr_main(main_grp,"Offset_CTL",offset_ctl)
        else:
            cmds.delete(offset_ctl)
            
        if bool_driverjnt:
            self.create_driver(follower_jnt_grp,driver_ctl,driver_jnt_grp)
            self.create_attr_main(main_grp,"Driver_JNT",driver_jnt_grp)
            if self.CB_createctldriver.isChecked():
                self.create_attr_main(main_grp,"Driver_CTL",driver_ctl)
            
        else:
            cmds.delete([driver_ctl,driver_jnt_grp])
            if not bool_offsetctl:
                if bool_followerjnt:
                    self.constraint_jnts(follower_jnt_grp)
                
            
        if not bool_followerjnt:
            cmds.delete(follower_jnt_grp)
            cmds.deleteAttr(main_grp+".Offset_JNT_Vis")
          
          
        if bool_driverjnt:
            self.bind_jnts(driver_jnt_grp,name_loft)
        elif bool_followerjnt:
            self.bind_jnts(follower_jnt_grp,name_loft)
        else:
            self.bind_jnts(None,name_loft)
        
          
    def create_uvpin(self,follower_jnt_grp,name_loft):
        
        cmds.select(cl=True)
        
        children_follower_jnt = cmds.listRelatives(follower_jnt_grp,children=True)
        
        cmds.select(name_loft,add=True)

        for child in children_follower_jnt:
            print child
            child = self.get_path_name(follower_jnt_grp,child)
            cmds.select(child,add=True)
          
        cmds.UVPin()
        for child in children_follower_jnt:
            child = self.get_path_name(follower_jnt_grp,child)
            cmds.setAttr(child+".jointOrientX",0)
          
    def bind_jnts(self,parent_grp,name_loft):
        
        if parent_grp:
            children = cmds.listRelatives(parent_grp,children=True)
            children = [self.get_path_name(parent_grp,x) for x in children]
        else:
            children = self.list_path_correct
        cmds.skinCluster(children, name_loft, name='Skin_Cluster_'+self.getABSname(name_loft), toSelectedBones=True, bindMethod=0, skinMethod=0, normalizeWeights=1)
          
    def constraint_jnts(self,follower_jnt_grp):
        
        children_follower_jnt = cmds.listRelatives(follower_jnt_grp,children=True)
        children_follower_jnt.reverse()
        for jnt_index in range(len(children_follower_jnt)):
            child = self.get_path_name(follower_jnt_grp,children_follower_jnt[jnt_index])
            cmds.parentConstraint(child,self.list_path_correct[jnt_index],mo=True)
          
    def create_grps(self):
        
        main_grp = cmds.createNode("transform",n="Main_ribbon_{0}_GRP".format(self.start_name))
        nurbs_grp = cmds.createNode("transform",n="NURBS_ribbon_{0}_GRP".format(self.start_name))
        CTL = cmds.createNode("transform",n="CTL_ribbon_{0}_GRP".format(self.start_name))
        JNT = cmds.createNode("transform",n="JNT_ribbon_{0}_GRP".format(self.start_name))
        follower_jnt_grp = cmds.createNode("transform",name = "Follower_ribbon_{0}_JNT_GRP".format(self.start_name))
        offset_ctl = cmds.createNode("transform",name = "Offset_ribbon_{0}_CTL_GRP".format(self.start_name))
        
        driver_jnt_grp = cmds.createNode("transform",name = "Driver_ribbon_{0}_JNT_GRP".format(self.start_name))
        driver_ctl = cmds.createNode("transform",name = "Driver_ribbon_{0}_CTL_GRP".format(self.start_name))
        
        
        cmds.parent(nurbs_grp,main_grp)
        cmds.parent(CTL,main_grp)
        cmds.parent(JNT,main_grp)
        
        CTL = self.get_path_name(main_grp,CTL)
        JNT = self.get_path_name(main_grp,JNT)
        
        cmds.parent(follower_jnt_grp,JNT)
        cmds.parent(offset_ctl,CTL)
        
        offset_ctl = self.get_path_name(CTL,offset_ctl)
        follower_jnt_grp = self.get_path_name(JNT,follower_jnt_grp)
        
        cmds.parent(driver_jnt_grp,JNT)
        cmds.parent(driver_ctl,CTL)
        
        driver_ctl = self.get_path_name(CTL,driver_ctl)
        driver_jnt_grp = self.get_path_name(JNT,driver_jnt_grp)
        
        nurbs_grp = self.get_path_name(main_grp,nurbs_grp)
        
        
        
        return [offset_ctl,follower_jnt_grp,nurbs_grp,driver_ctl,driver_jnt_grp,main_grp]
        
      
    def create_attr_main(self,main_grp,ln,input_obj):
        
        name_attr = cmds.addAttr(main_grp ,ln = "{0}_Vis".format(ln),at = 'bool' , keyable = True)
        cmds.setAttr("{0}.{1}_Vis".format(main_grp,ln),1)
        input_obj = input_obj+".visibility"
        cmds.connectAttr("{0}.{1}_Vis".format(main_grp,ln),input_obj)
        
         
    def create_driver(self,follower_jnt_grp,driver_ctl,driver_jnt_grp):
        
        jnts_follower_path = self.get_main_jnts_path_list(follower_jnt_grp)
        count_joints = len(self.list_correct_joints)
        if count_joints%2 !=0:
            self.create_driver_minus(count_joints , jnts_follower_path , driver_ctl , driver_jnt_grp)
        else:
            self.create_driver_plus(count_joints , jnts_follower_path , driver_ctl , driver_jnt_grp)
         
         
    def create_driver_plus(self, count_joints , jnts_follower_path , driver_ctl , driver_jnt_grp):
        
        value = self.IS_numbdriverjnt.value()
        bool_ctl_driver = self.CB_createctldriver.isChecked()
        
        index_last_jnt = self.list_correct_joints.index(self.end_name)
        dis_drivers   =  int(round(float(count_joints)/float(value)))
        center_index_right = int(round( count_joints / 2 ))
        center_index_left = int(round( count_joints / 2 ))-1
        
        if value%2 != 0:
            
            if value == 1:
                
                self.create_jnt_driver( center_index_left , bool_ctl_driver , driver_ctl , driver_jnt_grp )
                self.create_jnt_driver( center_index_right , bool_ctl_driver , driver_ctl , driver_jnt_grp )
            
            elif value == 3:
                
                self.create_jnt_driver( center_index_left , bool_ctl_driver , driver_ctl , driver_jnt_grp )
                self.create_jnt_driver( center_index_right , bool_ctl_driver , driver_ctl , driver_jnt_grp )
                self.create_jnt_driver( 0 , bool_ctl_driver , driver_ctl , driver_jnt_grp )
                self.create_jnt_driver( index_last_jnt , bool_ctl_driver , driver_ctl , driver_jnt_grp )
         
            else:
                
                self.create_jnt_driver( 0 , bool_ctl_driver , driver_ctl , driver_jnt_grp )
                self.create_jnt_driver( index_last_jnt , bool_ctl_driver , driver_ctl , driver_jnt_grp )
                
                left_to_center = 0 + dis_drivers
                right_to_center = index_last_jnt - dis_drivers
                
                while left_to_center < right_to_center:
                    
                    self.create_jnt_driver( left_to_center , bool_ctl_driver , driver_ctl , driver_jnt_grp )
                    
                    if len(cmds.listRelatives(driver_jnt_grp,children=True))>=value:
                        break
                    
                    self.create_jnt_driver( right_to_center , bool_ctl_driver , driver_ctl , driver_jnt_grp )
                    
                    if len(cmds.listRelatives(driver_jnt_grp,children=True))>=value:
                        break
                    
                    right_to_center-= dis_drivers
                    left_to_center+=dis_drivers
        else:
            
            if value == 2:
                
                self.create_jnt_driver( 0 , bool_ctl_driver , driver_ctl , driver_jnt_grp )
                self.create_jnt_driver( index_last_jnt , bool_ctl_driver , driver_ctl , driver_jnt_grp )
            
            else:
                
                self.create_jnt_driver( 0 , bool_ctl_driver , driver_ctl , driver_jnt_grp )
                self.create_jnt_driver( index_last_jnt , bool_ctl_driver , driver_ctl , driver_jnt_grp )
            
                left_to_center = 0 + dis_drivers
                right_to_center = index_last_jnt - dis_drivers
                
                while left_to_center < right_to_center:
                    
                    self.create_jnt_driver( left_to_center , bool_ctl_driver , driver_ctl , driver_jnt_grp )
                    
                    if len(cmds.listRelatives(driver_jnt_grp,children=True))>=value:
                        break
                    
                    self.create_jnt_driver( right_to_center , bool_ctl_driver , driver_ctl , driver_jnt_grp )
                    
                    if len(cmds.listRelatives(driver_jnt_grp,children=True))>=value:
                        break
                    
                    right_to_center-= dis_drivers
                    left_to_center+=dis_drivers
                
            
    def create_driver_minus(self, count_joints , jnts_follower_path , driver_ctl , driver_jnt_grp):
        
        value = self.IS_numbdriverjnt.value()
        bool_ctl_driver = self.CB_createctldriver.isChecked()
        
        index_last_jnt = self.list_correct_joints.index(self.end_name)
        dis_drivers   =  int(round(float(count_joints)/float(value)))
        center_index = int(round( count_joints / 2 ))
        
        if value % 2 != 0:
            
            
            
            if value == 1:
                
                self.create_jnt_driver( center_index , bool_ctl_driver , driver_ctl , driver_jnt_grp )
                
            elif value == 3:
                
                self.create_jnt_driver( center_index , bool_ctl_driver , driver_ctl , driver_jnt_grp )
                self.create_jnt_driver( 0 , bool_ctl_driver , driver_ctl , driver_jnt_grp )
                self.create_jnt_driver( index_last_jnt , bool_ctl_driver , driver_ctl , driver_jnt_grp )
                
            else:
                
                self.create_jnt_driver( center_index , bool_ctl_driver , driver_ctl , driver_jnt_grp )
                self.create_jnt_driver( 0 , bool_ctl_driver , driver_ctl , driver_jnt_grp )
                self.create_jnt_driver( index_last_jnt , bool_ctl_driver , driver_ctl , driver_jnt_grp )
                
                left_to_right = dis_drivers
                right_to_left = index_last_jnt-dis_drivers
                
                while center_index > left_to_right:
                    
                    self.create_jnt_driver( left_to_right , bool_ctl_driver , driver_ctl , driver_jnt_grp )
                    self.create_jnt_driver( right_to_left , bool_ctl_driver , driver_ctl , driver_jnt_grp )
                    
                    if len(cmds.listRelatives(driver_jnt_grp,children=True))==value:
                        break
                    
                    left_to_right+= dis_drivers
                    right_to_left-=dis_drivers
                    
                    
        else:
            
            if value == 2:
                
                self.create_jnt_driver( 0 , bool_ctl_driver , driver_ctl , driver_jnt_grp )
                self.create_jnt_driver( index_last_jnt , bool_ctl_driver , driver_ctl , driver_jnt_grp )
            
            else:

                self.create_jnt_driver( 0 , bool_ctl_driver , driver_ctl , driver_jnt_grp )
                self.create_jnt_driver( index_last_jnt , bool_ctl_driver , driver_ctl , driver_jnt_grp )
                
                left_to_center = 0 + dis_drivers
                right_to_center = index_last_jnt - dis_drivers
                
                while left_to_center < right_to_center:
                    
                    self.create_jnt_driver( left_to_center , bool_ctl_driver , driver_ctl , driver_jnt_grp )
                    
                    if len(cmds.listRelatives(driver_jnt_grp,children=True))>=value:
                        break
                    
                    self.create_jnt_driver( right_to_center , bool_ctl_driver , driver_ctl , driver_jnt_grp )
                    
                    if len(cmds.listRelatives(driver_jnt_grp,children=True))>=value:
                        break
                    
                    right_to_center-= dis_drivers
                    left_to_center+=dis_drivers
                
                
    def create_jnt_driver( self , index , bool_ctl_driver , driver_ctl , driver_jnt_grp ):
        
        parent_obj = self.list_path_correct[index-1]
        if index == 0:
            try:
                parent_obj = cmds.listRelatives(self.list_path_correct[index],parent = True)[0]
            except:
                parent_obj = ""
        
        name_driver_jnt = cmds.duplicate(self.list_path_correct[index],name = "{0}_driver_JNT".format(self.list_correct_joints[index]),returnRootsOnly=True)[0]
        name_driver_jnt = self.get_path_name(parent_obj,name_driver_jnt)
        self.delete_children(name_driver_jnt)
        
        
        if bool_ctl_driver:
            driver_locator = cmds.spaceLocator(name = "{0}_driver_CTL".format(self.list_correct_joints[index]) )[0]
            driver_locator = self.get_path_name("",driver_locator)
            driver_offset = cmds.createNode("transform",name = "{0}_driver_CTL_OFFSET".format(self.list_correct_joints[index]))
            driver_offset = self.get_path_name("",driver_offset)
            
            cmds.parent(driver_locator,driver_offset)
            driver_locator = self.get_path_name(driver_offset,driver_locator)
            
            const = cmds.parentConstraint(name_driver_jnt,driver_offset)[0]
            cmds.delete(self.get_path_name( driver_offset , const ))
            cmds.parentConstraint(driver_locator,name_driver_jnt)
            cmds.parent(driver_offset,driver_ctl)
            
        cmds.parent(name_driver_jnt,driver_jnt_grp)
        
        
    def delete_children(self,name_driver_jnt):
        
        children = cmds.listRelatives(name_driver_jnt,children=True)
        if children :
            for child in children :
                actual_name = self.get_path_name(name_driver_jnt,child)
                cmds.delete(actual_name)
        
    def create_offset(self,bool_followerjnt,follower_jnt_grp,offset_ctl):
            
        jnts_follower_path = self.get_main_jnts_path_list(follower_jnt_grp)
        self.create_loc_offset(jnts_follower_path,bool_followerjnt,offset_ctl)
        
        
        
    def create_loc_offset(self,jnts_follower_path,bool_followerjnt,offset_ctl):
        
        
        for index_jnt in range(len(jnts_follower_path)):
            
            loc = cmds.spaceLocator(name = "{0}_CTL".format(self.getABSname(self.list_path_correct[index_jnt])))[0]
            offset_node = cmds.createNode("transform",name = "{0}_OFFSET".format(loc))
            
            loc = self.get_path_name("",loc)
            offset_node = self.get_path_name("",offset_node)
            
            cmds.parent(loc,offset_node)
            loc = self.get_path_name(offset_node,self.getABSname(loc))
            
            const_offset = cmds.parentConstraint(self.list_path_correct[index_jnt],offset_node,mo=False)[0]
            cmds.delete(const_offset)
            const_offset = cmds.parentConstraint(jnts_follower_path[index_jnt],offset_node,mo=True)[0]
            const_offset = self.get_path_name(offset_node,const_offset)
            if not bool_followerjnt:
                cmds.delete(const_offset)
            cmds.parentConstraint(loc , self.list_path_correct[index_jnt],mo=True)
            cmds.parent(offset_node,offset_ctl)
        
        
    def create_follower_jnt(self,follower_jnt_grp):
        
        follower_jnts = cmds.duplicate(self.start_long_name,name="{0}".format(self.start_name))
        parent_follower = self.child_jnt(follower_jnts[0],follower_jnts[0],"Offset",True,follower_jnt_grp,self.list_correct_joints[0])
        
        
    def child_jnt(self,jnt_name,actual_name , name_for_rename=None,rename=False,name_parent =None,first_name_jnt=None):
                
        childs = cmds.listRelatives(jnt_name,children=True)
        if childs:
            for child in childs:
                child_path = self.get_path_name(jnt_name,child)
                if not child in self.list_correct_joints:
                    cmds.delete(child_path)
                    continue

                self.child_jnt(child_path,child,"Offset",True,name_parent)
            
        cmds.parent(jnt_name,name_parent)
        if rename:
            jnt_name=self.get_path_name(name_parent,actual_name)
            if first_name_jnt:
                actual_name = first_name_jnt
            cmds.rename(jnt_name,"{0}_{1}_JNT".format(name_for_rename,actual_name))
        
        
    def create_nurbs_loft(self,positions):
        
        normal_jnt = self.get_checkboxnormal()
        if normal_jnt == "x":
            nr_val = (-90,0,0)
        elif normal_jnt =="y":
            nr_val = (0,-90,0)
        else:
            nr_val = (0,0,-90)
            
        if self.CB_reverse.currentText() == "+":
            nr_val=tuple([-1*x for x in nr_val])
        
        radius = self.get_radius_value()
        main_curve = cmds.curve(d=1,p=positions,name = "main_curve_ribbon")
        offset_curve_1 = cmds.offsetCurve(main_curve,ch=0,rn=False,cb=2,st=True,cl=True,cr=0,d=radius,tol= 0.01,sd=5,ugn = True,nr=nr_val)[0]
        offset_curve_2 = cmds.offsetCurve(main_curve,ch=0,rn=False,cb=2,st=True,cl=True,cr=0,d=-radius,tol= 0.01,sd=5,ugn = True,nr=nr_val)[0]
            
        name_loft = cmds.loft(offset_curve_1,offset_curve_2,ch=0,u=1,c=0,ar=1,d=3,ss = 1 , rn = 0,po = 0 ,rsn=True,name = "Loft_{0}".format(self.start_name))[0]
        cmds.delete([offset_curve_1,offset_curve_2,main_curve])
        return name_loft
        
        
        
    def set_joint_to_lineedit(self):
        
        ls_start_end_jnts_long = cmds.ls(sl=True,long=True)
        if len(ls_start_end_jnts_long) == 2:
            if self.check_start_end_joints(ls_start_end_jnts_long):
                self.set_text_lineedit(ls_start_end_jnts_long)
                self.get_path_list()
        else:
            om.MGlobal.displayError("Select two joints and set")
            raise RuntimeError("Select two joints and set")
            
    
    def check_line_edit_exist(self):
        
        
        text = self.LE_endjnt.text()
        if not text:
            om.MGlobal.displayError("First set joints")
            raise RuntimeError("First set joints")
        return True
    
    
    
    def check_start_end_joints(self,ls_start_end_jnts):
        
        end_jnt_long = ls_start_end_jnts[-1]
        start_jnt_long = ls_start_end_jnts[0]
        
        for jnt in ls_start_end_jnts:
            if not cmds.objectType(jnt) == "joint":
                om.MGlobal.displayError("Just select joint objects")
                raise RuntimeError("Just select joint objects")
                
        
        ABS_start_jnt = self.getABSname(start_jnt_long)
        list_hierarchy_parent_endjnt = end_jnt_long.split("|")
        if not ABS_start_jnt in list_hierarchy_parent_endjnt:
            om.MGlobal.displayError("First select start joint and then select end joint .")
            raise RuntimeError("First select start joint and then select end joint .")
        else:
            self.set_correct_list(list_hierarchy_parent_endjnt,ABS_start_jnt)
        return True
        
        
    def set_maxi_min_driver(self):
        
        
        len_jnts = len(self.list_correct_joints)
        self.IS_numbdriverjnt.setMinimum(1)
        self.IS_numbdriverjnt.setMaximum(len_jnts)
        
    def set_correct_list(self,list_incorrect,start_joint):
        
        index_start_jnt = list_incorrect.index(start_joint)
        del list_incorrect[0:index_start_jnt]
        self.list_correct_joints = list_incorrect
        
        
        
    def set_text_lineedit(self,long_names):
        
        self.start_name = self.getABSname(long_names[0])
        self.end_name = self.getABSname(long_names[1])
        
        self.LE_startjnt.setText(self.start_name)
        self.LE_endjnt.setText(self.end_name)
        
        self.start_long_name = long_names[0]
        self.end_long_name = long_names[1]
        
        
    def get_path_list(self):
        
        
        self.list_path_correct = []
        for jnt_index in range(len(self.list_correct_joints)):
            if jnt_index == 0:
                self.list_path_correct.append(self.start_long_name)
            else:
                self.list_path_correct.append(self.get_path_name(self.list_path_correct[jnt_index-1],self.list_correct_joints[jnt_index]))
        return self.list_path_correct
        
        
        
    def get_path_name(self,jnt_name,child):
        return jnt_name+"|"+child
    
    
    def get_radius_value(self):
        return float("%.3f"%cmds.getAttr(self.start_long_name+".radius"))
        
    
    def get_main_jnts_path_list(self,name_grp):
        
        jnts= []
        for jnt in cmds.listRelatives(name_grp,allDescendents=True):
            jnts.append(self.get_path_name(name_grp,jnt))
        jnts.reverse()
        return jnts
    
    
    def get_positions_joints(self,parent_follower):
    
        positions= []
        for jnt_follower in cmds.listRelatives(parent_follower,allDescendents=True):
            positions.append(cmds.xform(parent_follower+"|"+jnt_follower,translation=True,q=True,ws=True))
        
        return positions
        
        
    def getABSname(self,long_name):
        
        if long_name:
            list_long_name = long_name.split("|")
            ABS_name = list_long_name[-1]
            return ABS_name
        
        
        
    def get_end_lineedit(self):
        
        jnt = self.LE_endjnt()
        if jnt:
            return jnt
        else:
            om.MGlobal.displayError("Set start and end joints")
            raise RuntimeError("Set start and end joints")



    def get_start_lineedit(self):
        
        jnt = self.LE_startjnt()
        if jnt:
            return jnt
        else:
            om.MGlobal.displayError("Set start and end joints")
            raise RuntimeError("Set start and end joints")



    def get_checkboxnormal(self):
        
        if self.RB_x.isChecked():
            return "x"
        elif self.RB_y.isChecked():
            return "y"
        else:
            return "z"

