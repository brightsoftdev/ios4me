/* 
 * Copyright (C) 2009 Smart&Soft.
 * All rights reserved.
 *
 * The code hereby is the full property of Smart&Soft, SIREN 517 961 744.
 * http://www.smartnsoft.com - contact@smartnsoft.com
 * 
 * You are not allowed to use the source code or the resulting binary code, nor to modify the source code, without prior permission of the owner.
 */

//
//  SnSDelegate.h
//  SnSFramework
//
//  Created by Édouard Mercier on 18/12/2009.
//

#import <UIKit/UIKit.h>

#pragma mark -
#pragma mark SnSUtils

@interface SnSUtils : NSObject
{
}

/**
 * Use to detecte iPad device.
 */
+ (BOOL) isPad;
/**
 * Use to check validity of an email.
 **/
+ (BOOL) emailIsValid:(NSString *)email;
@end

#pragma mark -
#pragma mark SnSFontUtils

/**
 * To know list of font on device
 for (NSString * familyName in [UIFont familyNames]) {
 for (NSString * fontName  in [UIFont fontNamesForFamilyName:familyName]) {
 SnSLogD(@"familyName : %@  ; fontName : %@", familyName, fontName);
 }
 }
 **/
/*
 
 familyName : AppleGothic  ; fontName : AppleGothic
 familyName : Hiragino Kaku Gothic ProN  ; fontName : HiraKakuProN-W6
 familyName : Hiragino Kaku Gothic ProN  ; fontName : HiraKakuProN-W3
 familyName : Arial Unicode MS  ; fontName : ArialUnicodeMS
 familyName : Heiti K  ; fontName : STHeitiK-Medium
 familyName : Heiti K  ; fontName : STHeitiK-Light
 familyName : DB LCD Temp  ; fontName : DBLCDTempBlack
 familyName : Helvetica  ; fontName : Helvetica-Oblique
 familyName : Helvetica  ; fontName : Helvetica-BoldOblique
 familyName : Helvetica  ; fontName : Helvetica
 familyName : Helvetica  ; fontName : Helvetica-Bold
 familyName : Marker Felt  ; fontName : MarkerFelt-Thin
 familyName : Times New Roman  ; fontName : TimesNewRomanPSMT
 familyName : Times New Roman  ; fontName : TimesNewRomanPS-BoldMT
 familyName : Times New Roman  ; fontName : TimesNewRomanPS-BoldItalicMT
 familyName : Times New Roman  ; fontName : TimesNewRomanPS-ItalicMT
 familyName : Verdana  ; fontName : Verdana-Bold
 familyName : Verdana  ; fontName : Verdana-BoldItalic
 familyName : Verdana  ; fontName : Verdana
 familyName : Verdana  ; fontName : Verdana-Italic
 familyName : Georgia  ; fontName : Georgia-Bold
 familyName : Georgia  ; fontName : Georgia
 familyName : Georgia  ; fontName : Georgia-BoldItalic
 familyName : Georgia  ; fontName : Georgia-Italic
 familyName : Arial Rounded MT Bold  ; fontName : ArialRoundedMTBold
 familyName : Trebuchet MS  ; fontName : TrebuchetMS-Italic
 familyName : Trebuchet MS  ; fontName : TrebuchetMS
 familyName : Trebuchet MS  ; fontName : Trebuchet-BoldItalic
 familyName : Trebuchet MS  ; fontName : TrebuchetMS-Bold
 familyName : Heiti TC  ; fontName : STHeitiTC-Light
 familyName : Heiti TC  ; fontName : STHeitiTC-Medium
 familyName : Geeza Pro  ; fontName : GeezaPro-Bold
 familyName : Geeza Pro  ; fontName : GeezaPro
 familyName : Courier  ; fontName : Courier
 familyName : Courier  ; fontName : Courier-BoldOblique
 familyName : Courier  ; fontName : Courier-Oblique
 familyName : Courier  ; fontName : Courier-Bold
 familyName : Arial  ; fontName : ArialMT
 familyName : Arial  ; fontName : Arial-BoldMT
 familyName : Arial  ; fontName : Arial-BoldItalicMT
 familyName : Arial  ; fontName : Arial-ItalicMT
 familyName : Heiti J  ; fontName : STHeitiJ-Medium
 familyName : Heiti J  ; fontName : STHeitiJ-Light
 familyName : Arial Hebrew  ; fontName : ArialHebrew
 familyName : Arial Hebrew  ; fontName : ArialHebrew-Bold
 familyName : Courier New  ; fontName : CourierNewPS-BoldMT
 familyName : Courier New  ; fontName : CourierNewPS-ItalicMT
 familyName : Courier New  ; fontName : CourierNewPS-BoldItalicMT
 familyName : Courier New  ; fontName : CourierNewPSMT
 familyName : Zapfino  ; fontName : Zapfino
 familyName : American Typewriter  ; fontName : AmericanTypewriter
 familyName : American Typewriter  ; fontName : AmericanTypewriter-Bold
 familyName : Heiti SC  ; fontName : STHeitiSC-Medium
 familyName : Heiti SC  ; fontName : STHeitiSC-Light
 familyName : Helvetica Neue  ; fontName : HelveticaNeue
 familyName : Helvetica Neue  ; fontName : HelveticaNeue-Bold
 familyName : Thonburi  ; fontName : Thonburi-Bold
 familyName : Thonburi  ; fontName : Thonburi
 
 */


#define FONT(s) [UIFont fontWithName:@"Helvetica" size:s]
#define FONT_BOLD(s) [UIFont fontWithName:@"Helvetica-Bold" size:s]
#define FONT_ITALIC(s) [UIFont fontWithName:@"Helvetica-Oblique" size:s]
#define FONT_ARIAL(s) [UIFont fontWithName:@"ArialMT" size:s]
#define FONT_ARIAL_BOLD(s) [UIFont fontWithName:@"Arial-BoldMT" size:s]
#define FONT_ARIAL_ITALIC(s) [UIFont fontWithName:@"Arial-ItalicMT" size:s]
#define FONT_TIMES(s) [UIFont fontWithName:@"TimesNewRomanPSMT" size:s]
#define FONT_TIMES_BOLD(s) [UIFont fontWithName:@"TimesNewRomanPS-BoldMT" size:s]
#define FONT_TIMES_ITALIC(s) [UIFont fontWithName:@"TimesNewRomanPS-ItalicMT" size:s]
#define FONT_HELVETICA(s) [UIFont fontWithName:@"Helvetica" size:s]
#define FONT_HELVETICA_BOLD(s) [UIFont fontWithName:@"Helvetica-Bold" size:s]
#define FONT_HELVETICA_ITALIC(s) [UIFont fontWithName:@"Helvetica-Oblique" size:s]

@interface SnSFontUtils : NSObject
{
}

/** 
 * Add x point to a spécific font.
 */
+ (UIFont *)updateFontSize:(UIFont *)font addPointSize:(CGFloat)point;

@end


#pragma mark -
#pragma mark SnSColorUtils

#define RGB(r, g, b) [UIColor colorWithRed:r/255.0 green:g/255.0 blue:b/255.0 alpha:1]
#define RGBA(r, g, b, a) [UIColor colorWithRed:r/255.0 green:g/255.0 blue:b/255.0 alpha:a]
#define COLOR_HEXA(color) [SnSColorUtils colorFromWebColor:color]

/**
 * Tool to use and define colors. 
 */
@interface SnSColorUtils : NSObject
{
  
}

+ (UIColor *) colorFromWebColor:(NSString *)color;

@end


#pragma mark -
#pragma mark SnSDateUtils

@interface SnSDateUtils : NSObject
{
	
}

/**
 * Parsing of a date in a ISO8601 format.
 **/
+ (NSDate *) dateFromISO8601:(NSString *) str;
/**
 * Format a date in a specify pattern
 * Pattern must be in Unicode standard : http://unicode.org/reports/tr35/tr35-6.html#Date_Format_Patterns
 **/
+ (NSString *) formatDate:(NSDate *)date withPattern:(NSString *) pattern withLocale:(NSLocale *)locale;

+ (NSDate *) parseString:(NSString *)string withPattern:(NSString *)pattern withLocale:(NSLocale *)locale;
@end



#pragma mark -
#pragma mark SnSUILabelUtils

@interface SnSUILabelUtils : NSObject
{
}

/**
 * Resize of a UILabel using its width and fixing the vertical alignement.
 **/
+ (void)resizeLabelHeight:(UILabel *)myLabel usingVerticalAlign:(int)vertAlign;

/**
 * Resize of a UILabel with a fixed width and vertical alignement.
 **/
+ (void)setUILabel:(UILabel *)myLabel withMaxWidth:(CGFloat)maxWidth withText:(NSString *)theText usingVerticalAlign:(int)vertAlign;

/**
 * Resize of a UILabel in a specified frame and fixing the vertical alignement.
 **/
+ (void)setUILabel:(UILabel *)myLabel withMaxFrame:(CGRect)maxFrame withText:(NSString *)theText usingVerticalAlign:(int)vertAlign;

@end


#pragma mark -
#pragma mark SnSImageUtils


@interface SnSImageUtils : NSObject
{
	
}

/**
 * Make an image from 2 images using the size of the biggest.
 **/
+ (UIImage*) addImage:(UIImage*)firstImage andOtherImage:(UIImage *)secondImage;

/**
 * Center an image in a specified frame.
 **/
+ (UIImage *) centerImage:(UIImage *)image inFrame:(CGRect)frame;
/**
 * Rotate image to have the right orientation in a scale with the maxWidth.
 **/
+ (UIImage *)scaleAndRotateImage:(UIImage *)image andMaxSizeWidth:(int)maxWidth;
/**
 * Obtain image from ressources with its name using optimisation according device and iOS version.
 **/
+ (UIImage *) imageNamed:(NSString *)name;
+ (UIImage *) imageNamed:(NSString *)name withExtention:(NSString *)extention;
@end



